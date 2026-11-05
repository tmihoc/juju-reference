# Manifest version 3 (proposal, not applied): changes from the identifying-key principle (E38c)

Rule: a weak table (a foreign key column in its primary key) has its home on its owner's page; the page that names the concept points to it. Each row below changes only the home of one table; nothing else in version 2 changes.

| table | version 2 home | version 3 home (owner) | note |
|---|---|---|---|
| annotation_charm | annotation | charm | judge agrees |
| annotation_unit | annotation | unit | judge agrees |
| (six more annotation tables) | annotation | application, machine, model, storage (the owners) | the schema comments out their foreign keys; the key (uuid, key) shows the owner |
| cloud_defaults | model-defaults | cloud | judge: either |
| cloud_region_defaults | model-defaults | cloud | judge: either |
| log_transfer_progress | model-migration | model | judge: own page (migration checkpoint) |
| application_remote_offerer_relation_macaroon | offer | relation | judge agrees |
| model_secret_backend | secret-backend | model | judge agrees |
| machine_virtual_ssh_host_key | ssh | machine | judge agrees |
| unit_virtual_ssh_host_key | ssh | unit | judge agrees |
| application_storage_directive | storage | application | contradicts E34 audit and the existing storage page; two-home case |
| unit_storage_directive | storage | unit | same |

Effect: the `annotation`, `model-defaults`, `ssh`, `secret-backend` and `model-migration` pages shrink and become pointers or small pages; the owner pages gain sections. Review before applying; the three judge disagreements and the two storage-directive rows are the ones to look at.
