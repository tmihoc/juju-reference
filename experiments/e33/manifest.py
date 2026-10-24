# E34: the grouping manifest (hypothesis). Authored from first-word defaults plus reviewed overrides; output is an explicit table -> page file.
import sys,re,json,collections
sys.path.insert(0,'../e15')
import e15
S=('model','controller')
V={s:e15.parse(e15.NEW[s]) for s in S}
tabs={}
for s in S:
    for t,b in V[s]['tables'].items():
        d=tabs.setdefault(t,dict(scopes=set(),body='')); d['scopes'].add(s); d['body']+=' '+b
typing={t:{s:e15.typing(V[s],t) for s in tabs[t]['scopes']} for t in tabs}
lookup={t for t in tabs if all(typing[t][s]['lookup'] for s in typing[t])}-{'space'}
life={t for t in tabs if any(typing[t][s]['life'] for s in typing[t])}
fk={t:set(re.findall(r'REFERENCES\s+"?(\w+)',tabs[t]['body']))-{t} for t in tabs}
nonlook=sorted(t for t in tabs if t not in lookup)
PAGES={ # name: (kind, one sentence)
 'application':('noun','A deployed application: its configuration, endpoints, scale, status and platform.'),
 'unit':('noun','A unit of an application: its agent, status, state and resolution.'),
 'machine':('noun','A machine or container that hosts units: its cloud instance, placement, status, agent and block devices.'),
 'relation':('noun','A relation between application endpoints: its units, settings data bags and status.'),
 'storage':('noun','Charm storage: storage instances, volumes, filesystems, pools, directives and attachments.'),
 'model':('noun','A model: its identity, type, configuration, life and agent.'),
 'model-migration':('mechanism','Moving a model to another controller: phases, targets, progress.'),
 'secret':('noun','Secrets and their revisions, owners, consumers, permissions and rotation.'),
 'secret-backend':('noun','Where secret content is stored: backend registration, configuration, rotation.'),
 'charm':('noun','A charm as stored by Juju: metadata, actions, config, resources, storage declarations.'),
 'resource':('noun','Charm resources as attached to applications and units, with their file and image stores.'),
 'action':('noun','Running actions and execs: operations, tasks, their parameters, output and status.'),
 'offer':('noun','Cross-model offers and the remote application proxies that consume them.'),
 'cloud':('noun','Clouds and their regions, types and certificates.'),
 'credential':('noun','Cloud credentials and their attributes.'),
 'model-defaults':('noun','Default model configuration per cloud and region.'),
 'image-metadata':('noun','Cached cloud image metadata.'),
 'controller':('noun','The controller and its nodes: addresses, passwords, configuration, certificates cache.'),
 'upgrade':('mechanism','Controller upgrade state across controller nodes.'),
 'user':('noun','Users, their authentication and last login.'),
 'permission':('noun','Access levels granted to users on clouds, controllers, models and offers.'),
 'ssh-key':('noun','Public SSH keys users store and the models that authorise them.'),
 'ssh':('noun','SSH access to machines and units: host keys, connection requests, the SSH server port.'),
 'object-store':('noun','The object store backend, metadata, placement and drain.'),
 'agent-version':('noun','The model target agent version, stream and the agent binary catalogue.'),
 'space':('noun','Network spaces.'),
 'subnet':('noun','Subnets and their provider network ids.'),
 'zone':('noun','Availability zones and their subnets.'),
 'link-layer-device':('noun','Network devices, addresses and the network node of a machine or unit.'),
 'external-controller':('noun','Other controllers known for cross-controller relations and migration.'),
 'constraint':('facet','Constraints of models, machines and applications: the stored constraint, spaces, tags, zones.'),
 'annotation':('facet','Key-value annotations attached to entities.'),
 'status':('facet','The shared vocabulary of statuses across entities.'),
 'block-command':('mechanism','Operation blocks that guard the model.'),
 'removal':('mechanism','Scheduled removal jobs.'),
 'lease':('mechanism','Leases and leadership claims.'),
 'port':('noun','Opened port ranges of units.'),
 'telemetry':('noun','Tracing and logging configuration sent to external systems.'),
 'database':('substrate','Database bookkeeping: change log, namespaces, sequences, feature flags.'),
}
DEFAULT={ # first word -> page
 'application':'application','charm':'charm','machine':'machine','unit':'unit','relation':'relation','storage':'storage','secret':'secret','resource':'resource',
 'operation':'action','cloud':'cloud','controller':'controller','model':'model','annotation':'annotation','constraint':'constraint','user':'user','permission':'permission',
 'subnet':'subnet','availability':'zone','link':'link-layer-device','net':'link-layer-device','ip':'link-layer-device','fqdn':'link-layer-device','hostname':'link-layer-device',
 'offer':'offer','external':'external-controller','change':'database','namespace':'database','sequence':'database','flag':'database','lease':'lease','port':'port','removal':'removal',
 'autocert':'controller','bakery':'user','macaroon':'user','logging':'telemetry','workload':'telemetry','upgrade':'upgrade','space':'space','object':'object-store','agent':'agent-version',
 'ssh':'ssh','device':'application','instance':'machine','operator':'application','pending':'resource','log':'model-migration','k8s':'unit','block':'storage','provider':'subnet',
}
OVERRIDE={ # table -> (page, reason)
 'model_migrating':('model-migration','marks a migration in progress (E33 audit)'),
 'model_secret_backend':('secret-backend','maps a model to its secret backend (E33 audit)'),
 'model_authorized_keys':('ssh-key','links keys to models (E33 audit; keymanager)'),
 'model_last_login':('user','a user attribute (E33 audit)'),
 'model_storage_pool':('storage','default pool per storage kind (E33 audit)'),
 'secret_backend':('secret-backend','a controller-level noun, not a model secret (E33 audit)'),
 'secret_backend_config':('secret-backend','(E33 audit)'),'secret_backend_reference':('secret-backend','(E33 audit)'),'secret_backend_rotation':('secret-backend','(E33 audit)'),
 'cloud_credential':('credential','own domain and facade (E33 audit)'),'cloud_credential_attribute':('credential','(E33 audit)'),
 'cloud_defaults':('model-defaults','model defaults noun (E33 audit)'),'cloud_region_defaults':('model-defaults','(E33 audit)'),
 'cloud_image_metadata':('image-metadata','own domain (E33 audit)'),
 'application_remote_offerer':('offer','remote application proxy of a cross-model offer (E33 audit)'),'application_remote_offerer_status':('offer','(E33 audit)'),
 'application_remote_offerer_relation_macaroon':('offer','(E33 audit)'),'application_remote_consumer':('offer','(E33 audit)'),
 'application_resource':('resource','link table between application and resource (E33 audit)'),
 'unit_resource':('resource','link table between unit and resource (same reason)'),
 'k8s_service':('application','the Kubernetes service of an application'),
 'machine_volume':('storage','join between a machine and a storage volume (E33 audit)'),'machine_filesystem':('storage','(E33 audit)'),
 'machine_ssh_host_key':('ssh','host keys of machines belong with the other host keys'),
 'ssh_connection_request':('ssh','(E33 audit)'),'machine_virtual_ssh_host_key':('ssh','(E33 audit)'),'unit_virtual_ssh_host_key':('ssh','(E33 audit)'),
 'controller_ssh_host_key':('ssh','host key of the controller'),'controller_ssh_server_port':('ssh','SSH server port'),
 'log_transfer_progress':('model-migration','checkpoint of migration log transfer (E33 audit)'),
 'upgrade_info':('upgrade','(E33 audit)'),'upgrade_info_controller_node':('upgrade','(E33 audit)'),
 'user_public_ssh_key':('ssh-key','a user\'s public key'),
 'agent_binary_store':('agent-version','agent binary catalogue (E33 audit)'),
 'block_command':('block-command','a guard, not a device (E33 audit)'),
 'charm_tracing_config':('telemetry','controller tracing configuration, not a charm fact'),
 'provider_space':('space','provider id of a space (E33 audit)'),'provider_subnet':('subnet','(E33 audit)'),'provider_network':('subnet','(E33 audit)'),'provider_network_subnet':('subnet','(E33 audit)'),
 'provider_ip_address':('link-layer-device','(E33 audit)'),'provider_link_layer_device':('link-layer-device','(E33 audit)'),
 'availability_zone':('zone','own page upstream (E33 audit)'),'availability_zone_subnet':('zone','(E33 audit)'),
 'constraint_space':('constraint','(constraint facet)'),
 'permission':('permission','(E33 audit)'),'permission_object_access':('permission','(E33 audit)'),
 'removal':('removal','(mechanism)'),'application_constraint':('application','link of an entity to a constraint stays with the entity (facet rule)'),
 'machine_constraint':('machine','(facet rule)'),'model_constraint':('model','(facet rule)'),
 'controller_config':('controller','(configuration of the controller)'),
 'bakery_config':('controller','macaroon bakery keys of the controller; no foreign key to a user (E34 M2, verified)'),'macaroon_root_key':('controller','macaroon root keys; no foreign key to a user (E34 M2, verified)'),
 'flag':('controller','the only flag ever set is `bootstrapped`, by the bootstrap worker (E34 M2, verified)'),
 'block_device':('machine','a machine\'s disk inventory, foreign key machine (E34 M2, verified); storage points to it'),'block_device_link_device':('machine','(same reason)'),
 'application_storage_directive':('storage','storage directives are documented with storage; judge M1 and the existing storage page agree (E34 M1)'),'unit_storage_directive':('storage','(same reason)'),
 'model_database_deletion':('database','staging queue for the model database deleter, keyed by namespace, no foreign key to model (E34 M2, verified)'),
}
home={}
why={}
for t in nonlook:
    if t.startswith('model_migration'):
        home[t]='model-migration'; why[t]='the migration process, not the model (E33 audit)'; continue
    if t in OVERRIDE: home[t]=OVERRIDE[t][0]; why[t]=OVERRIDE[t][1]; continue
    p=DEFAULT.get(t.split('_')[0])
    if p is None: print('NO DEFAULT',t); continue
    home[t]=p
missing=[t for t in nonlook if t not in home]
bad=[t for t,p in home.items() if p not in PAGES]
# lookups: owned if every referrer in one page, else shared
lk={};shared=[]
for l in sorted(lookup):
    refs=[t for t in nonlook if l in fk[t]]
    ps={home[t] for t in refs if t in home}
    if l=='workload_status_value': lk[l]='status'
    elif len(ps)==1: lk[l]=next(iter(ps))
    elif l=='workload_status_value': lk[l]='status'
    elif not refs:
        fp=DEFAULT.get(l.split('_')[0]); (lk.__setitem__(l,fp) if fp in PAGES else shared.append(l))
    else: shared.append(l)
# attachments: foreign keys that cross pages (child page -> parent page) for context
cross=collections.Counter(); intra=0; total=0
for t in nonlook:
    for p in fk[t]:
        if p in home:
            total+=1
            if home[p]==home[t]: intra+=1
            else: cross[(home[t],home[p])]+=1
pg=collections.defaultdict(list)
for t,p in home.items(): pg[p].append(t)
json.dump(dict(pages={p:dict(kind=PAGES[p][0],about=PAGES[p][1],tables=sorted(pg.get(p,[])),lookups=sorted(l for l,x in lk.items() if x==p)) for p in PAGES},
  shared_vocabulary=sorted(shared),why=why),open('page-manifest.json','w'),indent=1)
print('non-lookup tables',len(nonlook),'assigned',len(home),'missing',missing,'bad page',bad)
print('pages',len(PAGES),'empty pages',[p for p in PAGES if not pg.get(p)]); print('shared vocabulary',sorted(shared))
print('cohesion (intra-page FK share among non-lookup tables): %d / %d = %.1f%%'%(intra,total,100*intra/total))
sizes=sorted(((p,len(pg[p])) for p in PAGES if pg.get(p)),key=lambda x:-x[1]); print(sizes)
print('small pages (<3):',[(p,n,PAGES[p][0]) for p,n in sizes if n<3])
