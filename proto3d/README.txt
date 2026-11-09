Player kit prototype (separate from the app; nothing in fantasy-gm.html uses it yet).
body_standing_hi.glb / _low.glb  the Standing model with its head removed (shared by every player)
head_A / head_C / head_D (.glb and _low.glb)  heads cut from the Standing, Brady and 40k skater models, each re-mapped onto its own small texture
meta.json  neck position and size of each head and body, used to fit any head on the body
gxkit.js   builds a player from { name, no, team, head, shoots, build, skin }: jersey colours and design, name and number, crest, helmet colour, mirrored for right shots
Files are compressed with EXT_meshopt_compression and WebP; vendor/gx3d.js includes the decoder.
