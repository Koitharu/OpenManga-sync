## Routes

##### User
```
/api/v1/user
```
| Method | Description             | Params                          | Auth required |
|--------|-------------------------|---------------------------------|---------------|
| GET    | Get all active sessions |           self: (1, 0)          |       +       |
| POST   | Sign in                 | login: String, password: String |               |
| PUT    | Sign up                 | login: String, password: String |               |
| DELETE | Close session           | self: (1, 0), id: Int           |       +       |

##### History
```
/api/v1/history
```
| Method | Description                                             | Params                   | Auth required |
|--------|---------------------------------------------------------|--------------------------|---------------|
| GET    | Get all history                                         |                          |       +       |
| POST   | Store new, updated and deleted items and return another | updated: [], deleted: [] |       +       |
| DELETE | Delete one item from history                            | id: Int                  |       +       |

##### Favourites
```
/api/v1/favourites
```
| Method | Description                                             | Params                   | Auth required |
|--------|---------------------------------------------------------|--------------------------|---------------|
| GET    | Get all favourites                                      |                          |       +       |
| POST   | Store new, updated and deleted items and return another | updated: [], deleted: [] |       +       |
| DELETE | Delete one item from favourites                         | id: Int                  |       +       |