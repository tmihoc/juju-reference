// E30: exposure by call graph. Usage: e30 <juju worktree> <tables.txt> <out.json>
package main

import (
	"encoding/json"
	"fmt"
	"go/constant"
	"go/types"
	"os"
	"regexp"
	"sort"
	"strings"

	"golang.org/x/tools/go/callgraph"
	"golang.org/x/tools/go/callgraph/cha"
	"golang.org/x/tools/go/callgraph/rta"
	"golang.org/x/tools/go/packages"
	"golang.org/x/tools/go/ssa"
	"golang.org/x/tools/go/ssa/ssautil"
)

const mod = "github.com/juju/juju/"

type Root struct {
	Kind   string `json:"kind"`   // facade, cli, hook, http, socket
	Tier   string `json:"tier"`   // client, agent, controller, ...
	Pkg    string `json:"pkg"`
	Name   string `json:"name"`
	Tables []string `json:"tables"`
	States []string `json:"states"` // domain state packages reached
	Funcs  int `json:"funcs"`
	Big    []string `json:"big"`
}

func main() {
	dir, tabFile, out := os.Args[1], os.Args[2], os.Args[3]
	tb, _ := os.ReadFile(tabFile)
	tables := strings.Fields(string(tb))
	re := regexp.MustCompile(`\b(` + strings.Join(tables, "|") + `)\b`)

	cfg := &packages.Config{
		Mode:  packages.LoadAllSyntax,
		Dir:   dir,
		Tests: false,
	}
	pats := []string{"./apiserver/...", "./cmd/juju/...", "./cmd/plugins/...", "./domain/...", "./internal/worker/uniter/runner/jujuc/...", "./internal/worker/controlsocket/..."}
	pkgs, err := packages.Load(cfg, pats...)
	if err != nil {
		fmt.Fprintln(os.Stderr, "load:", err)
		os.Exit(1)
	}
	nerr := 0
	packages.Visit(pkgs, nil, func(p *packages.Package) { nerr += len(p.Errors) })
	fmt.Fprintln(os.Stderr, "packages:", len(pkgs), "errors:", nerr)

	prog, _ := ssautil.AllPackages(pkgs, ssa.InstantiateGenerics)
	prog.Build()
	fmt.Fprintln(os.Stderr, "ssa built")
	var cg *callgraph.Graph
	_ = cha.CallGraph

	// tables per state function
	isState := func(path string) (string, bool) {
		if !strings.HasPrefix(path, mod+"domain/") {
			return "", false
		}
		rest := strings.TrimPrefix(path, mod+"domain/")
		parts := strings.Split(rest, "/")
		for i, p := range parts {
			if p == "state" {
				return parts[0] + "/" + strings.Join(parts[i:], "/"), true
			}
		}
		return "", false
	}
	fnTables := map[*ssa.Function][]string{}
	var tablesOf func(f *ssa.Function) []string
	tablesOf = func(f *ssa.Function) []string {
		if t, ok := fnTables[f]; ok {
			return t
		}
		set := map[string]bool{}
		var walk func(fn *ssa.Function)
		seen := map[*ssa.Function]bool{}
		walk = func(fn *ssa.Function) {
			if seen[fn] {
				return
			}
			seen[fn] = true
			for _, b := range fn.Blocks {
				for _, in := range b.Instrs {
					var ops []*ssa.Value
					ops = in.Operands(ops)
					for _, o := range ops {
						if o == nil {
							continue
						}
						if c, ok := (*o).(*ssa.Const); ok && c.Value != nil && c.Value.Kind() == constant.String {
							for _, m := range re.FindAllString(constant.StringVal(c.Value), -1) {
								set[m] = true
							}
						}
					}
				}
			}
			for _, af := range fn.AnonFuncs {
				walk(af)
			}
		}
		walk(f)
		var l []string
		for k := range set {
			l = append(l, k)
		}
		sort.Strings(l)
		fnTables[f] = l
		return l
	}

	var roots []*ssa.Function
	meta := map[*ssa.Function]Root{}
	add := func(f *ssa.Function, kind, tier string) {
		if f == nil {
			return
		}
		if _, dup := meta[f]; dup {
			return
		}
		pkg := ""
		if f.Pkg != nil {
			pkg = f.Pkg.Pkg.Path()
		}
		meta[f] = Root{Kind: kind, Tier: tier, Pkg: strings.TrimPrefix(pkg, mod), Name: f.String()}
		roots = append(roots, f)
	}
	for fn := range ssautil.AllFunctions(prog) {
		if fn.Pkg == nil || fn.Synthetic != "" || fn.Object() == nil {
			continue
		}
		path := fn.Pkg.Pkg.Path()
		if !strings.HasPrefix(path, mod) {
			continue
		}
		rel := strings.TrimPrefix(path, mod)
		if fn.Signature.Recv() == nil && !fn.Object().Exported() {
			continue
		}
		isMethod := fn.Signature.Recv() != nil
		exported := fn.Object() != nil && fn.Object().Exported()
		switch {
		case strings.HasPrefix(rel, "apiserver/facades/client/") || strings.HasPrefix(rel, "apiserver/facades/agent/") || strings.HasPrefix(rel, "apiserver/facades/controller/"):
			if isMethod && exported && fn.Signature.Params().Len() >= 1 {
				if t, ok := fn.Signature.Params().At(0).Type().(*types.Named); ok && t.Obj().Name() == "Context" {
					tier := strings.Split(rel, "/")[2]
					add(fn, "facade", tier)
				}
			}
		case strings.HasPrefix(rel, "cmd/juju/") || strings.HasPrefix(rel, "cmd/plugins/"):
			if isMethod && (fn.Name() == "Run" || fn.Name() == "Init") {
				add(fn, "cli", "cli")
			}
		case strings.HasPrefix(rel, "internal/worker/uniter/runner/jujuc"):
			if isMethod && fn.Name() == "Run" {
				add(fn, "hook", "hook")
			}
		case strings.HasPrefix(rel, "apiserver") && isMethod && fn.Name() == "ServeHTTP":
			add(fn, "http", "http")
		case strings.HasPrefix(rel, "internal/worker/controlsocket") && isMethod && fn.Name() == "ServeHTTP":
			add(fn, "socket", "socket")
		}
	}
	// facade methods including those promoted from embedded types
	for _, p := range prog.AllPackages() {
		path := p.Pkg.Path()
		if !(strings.HasPrefix(path, mod+"apiserver/facades/client/") || strings.HasPrefix(path, mod+"apiserver/facades/agent/") || strings.HasPrefix(path, mod+"apiserver/facades/controller/")) {
			continue
		}
		tier := strings.Split(strings.TrimPrefix(path, mod), "/")[2]
		for _, m := range p.Members {
			t, ok := m.(*ssa.Type)
			if !ok {
				continue
			}
			named, ok := t.Type().(*types.Named)
			if !ok {
				continue
			}
			if _, isIface := named.Underlying().(*types.Interface); isIface {
				continue
			}
			ms := prog.MethodSets.MethodSet(types.NewPointer(named))
			for i := 0; i < ms.Len(); i++ {
				sel := ms.At(i)
				fo, ok := sel.Obj().(*types.Func)
				if !ok || !fo.Exported() {
					continue
				}
				sig := fo.Type().(*types.Signature)
				if sig.Params().Len() < 1 {
					continue
				}
				if pt, ok := sig.Params().At(0).Type().(*types.Named); !ok || pt.Obj().Name() != "Context" {
					continue
				}
				fn := prog.MethodValue(sel)
				if fn == nil {
					continue
				}
				if _, dup := meta[fn]; dup {
					continue
				}
				meta[fn] = Root{Kind: "facade", Tier: tier, Pkg: strings.TrimPrefix(path, mod), Name: named.Obj().Name() + "." + fo.Name()}
				roots = append(roots, fn)
			}
		}
	}
	fmt.Fprintln(os.Stderr, "roots:", len(roots))
	var extra []*ssa.Function
	for fn := range ssautil.AllFunctions(prog) {
		if fn.Pkg == nil || fn.Synthetic != "" || fn.Object() == nil {
			continue
		}
		rel := strings.TrimPrefix(fn.Pkg.Pkg.Path(), mod)
		if rel == "domain/services" || strings.HasPrefix(rel, "domain/services/") {
			extra = append(extra, fn)
			continue
		}
		if strings.HasPrefix(rel, "domain/") && (strings.Contains(rel, "/service") || strings.Contains(rel, "/state")) && strings.HasPrefix(fn.Name(), "New") && fn.Signature.Recv() == nil {
			extra = append(extra, fn)
		}
	}
	fmt.Fprintln(os.Stderr, "extra rta roots:", len(extra))
	rr := rta.Analyze(append(append([]*ssa.Function{}, roots...), extra...), true)
	cg = rr.CallGraph
	fmt.Fprintln(os.Stderr, "rta callgraph nodes:", len(cg.Nodes))

	// BFS from each root, not traversing outside the module
	res := []Root{}
	for _, r := range roots {
		start := cg.Nodes[r]
		if start == nil {
			continue
		}
		seen := map[*callgraph.Node]bool{start: true}
		parent := map[*callgraph.Node]*callgraph.Node{}
		queue := []*callgraph.Node{start}
		tset := map[string]bool{}
		sset := map[string]bool{}
		n := 0
		var bigs []string
		for len(queue) > 0 {
			cur := queue[0]
			queue = queue[1:]
			n++
			if cur.Func.Pkg != nil {
				p := cur.Func.Pkg.Pkg.Path()
				if sp, ok := isState(p); ok {
					sset[sp] = true
					tl := tablesOf(cur.Func)
					if dt := os.Getenv("DEBUG_TABLE"); dt != "" && strings.Contains(r.String(), os.Getenv("DEBUG_ROOT")) && len(tl) < 20 {
						for _, t := range tl {
							if t == dt {
								fmt.Fprintln(os.Stderr, "PATH to", dt, "from", r.String())
								for x := cur; x != nil; x = parent[x] {
									fmt.Fprintln(os.Stderr, "   ", x.Func.String())
								}
								os.Exit(0)
							}
						}
					}
					if len(tl) >= 20 {
						bigs = append(bigs, cur.Func.String())
					}
					if len(tl) < 20 {
						for _, t := range tl {
							tset[t] = true
						}
					}
				}
			}
			for _, af := range cur.Func.AnonFuncs {
				if an := cg.Nodes[af]; an != nil && !seen[an] {
					seen[an] = true
					parent[an] = cur
					queue = append(queue, an)
				}
			}
			for _, e := range cur.Out {
				if e.Site != nil {
					if cc := e.Site.Common(); !cc.IsInvoke() && cc.StaticCallee() == nil {
						continue // call through a function value: not resolvable without over-approximation
					}
				}
				c := e.Callee
				if seen[c] || c.Func == nil {
					continue
				}
				cp := mod
				if c.Func.Pkg != nil {
					cp = c.Func.Pkg.Pkg.Path()
				} else if c.Func.Synthetic == "" {
					continue
				}
				if !strings.HasPrefix(cp, mod) {
					continue
				}
				// wiring and constructors would connect every root to every state package
				rel := strings.TrimPrefix(cp, mod)
				if rel == "domain/services" || strings.HasPrefix(rel, "domain/services/") || strings.HasPrefix(rel, "internal/worker/") || strings.HasPrefix(rel, "internal/database") || strings.HasPrefix(rel, "internal/provider/") || strings.HasPrefix(rel, "environs") || strings.HasPrefix(rel, "cmd/") {
					continue
				}
				if n := c.Func.Name(); strings.HasPrefix(n, "New") || strings.HasPrefix(n, "new") || n == "init" || strings.HasPrefix(n, "Register") {
					continue
				}
				seen[c] = true
				parent[c] = cur
				queue = append(queue, c)
			}
		}
		m := meta[r]
		for k := range tset {
			m.Tables = append(m.Tables, k)
		}
		for k := range sset {
			m.States = append(m.States, k)
		}
		sort.Strings(m.Tables)
		sort.Strings(m.States)
		m.Funcs = n
		m.Big = bigs
		res = append(res, m)
	}
	f, _ := os.Create(out)
	json.NewEncoder(f).Encode(res)
	f.Close()
	fmt.Fprintln(os.Stderr, "done:", len(res))
}
