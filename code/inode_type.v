Definition inode_type : Rec.type := Rec.RecF ([
  ("len",  Rec.WordF 64);     (* number of blocks *)
  ("attrs", iattr_type);      (* file attributes, another record type *)
  ("indptr", Rec.WordF 64);   (* indirect pointer *)
  ("blocks", Rec.ArrayF 9 (Rec.WordF 64))]). (* direct block pointers *)
