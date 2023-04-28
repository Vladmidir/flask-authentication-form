### H2 MySlq Notes:

MySql Stores files in the installation folder. For me it is E:\xampp\mysql\data\ {database-name}

Do not forget to mysql.connection.commit() to make sure the changes actually record in the database.
Also remember to cursor.close().

### H2 Flask Notes:

Do I really need to be escaping the form input? Does it make a difference, since the database should not care?
I should probably escape SQL injections to protect the database. I think I should escape the values I 
pull from the database. Or should I escape them when adding, so that I don't have to escape every single time
that I SELECT from the database? 

<mark> Anywas I should try to do some injections, before escaping and then see if escaping helps. </mark>

### H2 To Do Next:

I should probably add a route for the homepage and redirect there when a login is successful. I could make custom
home pages using information about the specific user form the database combined with Jinja template.