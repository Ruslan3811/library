# library-site
Making site for library using python/django

1) Realization of models in the "catalog" app :
For this models I used relations ManyToMany and OneToMany
![image](https://user-images.githubusercontent.com/68827287/140651427-654ab326-2803-4fd5-a316-3f13e0c074f2.png)

2) Using admin panel extensions

3) Making different permissions for users:
Using decorator @permission_required and mixin - PermissionRequiredMixin, I limited access to any pages for users.

4) It is configured an authentication and authorization of users.

5) Users can login, logout, see kinds of books, genres, authors,descriptions, create new books.

6) SuperUsers(librarian) can see status of books, who and when any person should return a book(this page is not visible for simple Users) and update information about date of returning book. If user is late, the librarian will notice this, as it will be highlighted in red text if someone has not returned by the due date.

7) In settings.py configured to send messages to the user's mail.

# Instruction of using the project:
  1) create .env in ./library/
  2) add into .env variables and values - DJANGO_SECRET_KEY, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
  3) activate the enviromental
  4) start using
