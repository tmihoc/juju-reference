# Endpoint boundary from runtime behavior -- E51

## Decision

The unresolved charm-vs-application choice was a false either/or. Keep **two linked, separately addressable facets**, not a new top-level endpoint page:

1. **Charm endpoint declaration** belongs with charm: its name, role, interface, scope and other declaration properties, including their validation and implicit declarations. They describe what a charm offers, requires or peers on.
2. **Application endpoint** belongs with application: an application-specific realization of one of its charm's endpoints, including its binding and exposure. Its stable address should be an application section, not hidden solely as an inspector-facing database record. Existing `(application-endpoint)` is the natural address to preserve. The calls that bind, expose or refresh an application keep their own conditions, outcomes and errors.
3. **Relation composition** belongs with relation: how application endpoints are matched and how their relation behaves. Link to the other two facets rather than redefine their contracts. Offer-specific publication belongs with offer.

This is a research decision about a candidate documentation structure, not authorization to modify docs or evidence for a generic page-per-facet rule. The existing application, charm and relation pages provide entry points; their precise section placement and text are subject to the earlier authorization requirement. The distinction comes from behavior below, not from existing pages, SQL layout or a competency question.

## Source evidence and limits

| Distinction | Evidence |
|---|---|
| Declaration | Charm metadata decodes `provides`, `requires` and `peers` (`domain/deployment/charm/meta.go:195-204,263-266,576-579`). The relation declaration supplies name, role, interface, scope, optionality and limit. |
| Application-specific realization | Application creation supplies the application UUID and requested bindings (`domain/application/state/application.go:331-333,370-378`). The endpoint-creation path reads that application's charm relations, resolves the application's bindings and constructs one application-qualified endpoint per charm relation (`domain/application/state/application_endpoint.go:341-378,398-433`). Two applications may use the same definition yet have distinct application endpoints. |
| Application-specific changes and observation | `MergeBindings` takes an application and binding changes (`apiserver/facades/client/application/application.go:2126-2162`). It resolves and updates only that application's bindings; absent force, changed bindings are validated against that application's units (`domain/application/state/application_endpoint.go:269-315,591-630`). `ApplicationsInfo` returns that application's endpoint bindings and exposure (`apiserver/facades/client/application/application.go:1935-1938,1982-1997,2065-2079`). Thus the same declaration does not determine a single space for all applications. |
| Refresh | On charm replacement, Juju checks existing relation compatibility and updates the application charm and endpoint bindings (`domain/application/state/application.go:1529-1539,1565-1574,1617-1627`). The refresh maps old endpoint names onto the new charm, removes missing endpoints, and creates new ones inheriting the application default unless subsequently bound (`domain/application/state/application_endpoint.go:992-1004,1063-1105`). This is a change to one application's realization, not a universal mutation of the old charm's declaration. |
| Relation | Relation creation infers application endpoints (`domain/relation/state/relation.go:80-111`); matching checks role and interface and additional scope/subordinate conditions and rejects zero or multiple matches (`domain/relation/state/relation.go:3605-3685`, `domain/relation/types.go:226-231`). A successful helper match alone is not a guarantee that relation creation succeeds. |
| Cross-model qualification | A remote representation uses its own synthetic charm/application and endpoint insertion path (`domain/crossmodelrelation/state/model/remoteapplication.go:385-427,618-660,729-777`). Do not treat the stored placeholder's alpha space as evidence of the remote application's actual network binding. |

For deployment and replacement, these are static traces through implementation and API; no live controller was exercised. Peer relations, extra bindings and implicit `juju-info` need their own exact conditions when authoring text. An extra binding is not automatically a relation endpoint (`application_endpoint.go:341-378`).

## Behavioral probe

A temporary Go program invoked the actual charm metadata parser and relation endpoint helper. With a charm declaring a `database` requirer on interface `postgresql`, it printed:

```text
charm endpoint: database role=requirer interface=postgresql
application endpoints: web-a:database, web-b:database
matching provider: web-a:database=true web-b:database=true
```

This exercises parsing, application-qualified naming and `CanRelateTo` for two constructed endpoints. It does **not** deploy applications, configure separate spaces, run full endpoint inference, or prove a relation can be created; those conclusions are source-traced and conditional on their respective validations. The script was removed.

## Scope compatibility: investigation, not a blanket conclusion

`docs/reference/application.md:421` says an existing relation needs the *same* scope in the new charm. The transactional refresh precheck rejects a change from global to container, but does not reject the reverse on scope alone (`domain/application/state/application.go:3639-3655`). A second throwaway Go probe of `charm.Relation.ImplementedBy` (`domain/deployment/charm/meta.go:206-236`) printed `global -> container: false` and `container -> global: true`. That helper is not the full application refresh path; this is strong source evidence that the wording may be too strict, **not** a live refresh or a proof that all other validation allows the reverse. Keep as a candidate correction until a valid end-to-end case is exercised. No docs were changed.

## Method outcome

E51's preregistered distinguishing condition supports structure C: a definition can have multiple application-scoped realizations with different observable settings, while a relation combines application endpoints. Do not ask the user to choose an owner merely because both are related: trace which behavior actually changes and split it at that semantic boundary. The exercise resolves the E50 endpoint-home tie at the contract level; it does not prove the complete endpoint inventory or globally validate the entity-reference form.
