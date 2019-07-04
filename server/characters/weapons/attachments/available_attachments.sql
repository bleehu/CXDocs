CREATE SEQUENCE available_attachments_pk_id_seq;

CREATE TABLE available_attachments (
    pk_id INTEGER PRIMARY KEY DEFAULT nextval('available_attachments_pk_id_seq'),
    name text NOT NULL,
    description text NOT NULL,
    slot text NOT NULL,
    full_auto_mod INTEGER,
    r1_mod INTEGER,
    r2_mod INTEGER,
    r3_mod INTEGER,
    hipfire_mod INTEGER,
    reflex_mod INTEGER,
    deleted_at timestamp
);

INSERT INTO available_attachments (name, slot, description, r1_mod, r2_mod, r3_mod) Values (
'Tritium Glow Iron Sights', 'Optics', 
'A metalic notch on the rear of the rail with a small metal post toward the muzzle, that serve as a simple way of lining up your shots. These particular metal sights have a streak of tritium paint on them so they glow softly like the marks on an old watch. 1x magnification, but allows for much better target acquisition. Can be mounted on 45 degree mounts in addition to a scope in order to negate a minimum engagement distance penalty.',
-1,-1,-1
);

INSERT INTO available_attachments (name, slot, description, hipfire_mod) VALUES (
'Red Laser', 'Laser', 'A small laser pointer that clips under the barrel of your gun and has been adjusted to roughly show where bullets go when you squeeze the trigger.',
-4
);

GRANT ALL  ON available_attachments TO searcher;
