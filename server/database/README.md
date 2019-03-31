# CX_Database

This module defines a generic database object from which the Character database 
and enemy database should inherit.

This helps keep our backend logic DRY and hopefully reduces the surface area 
that our psql adapter touches. Reducing this surface area hopefully makes it 
much easier to update that driver or switch from psql to MySQL and back.

The CXDatabase offers these methods

* fetch_all(queryString)
* fetch_first(queryString)
* update(updateString)
