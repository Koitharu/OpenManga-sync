## Routes

##### User
```
/api/user
```
| Method | Description                           | Params                         | Auth required | Result                                         |
|--------|---------------------------------------|--------------------------------|---------------|------------------------------------------------|
| GET    | Get all devices, associated with user |                -               |       +       | devices: [{ device: String, created_at: Long }] |
| POST   | Authorization                         | login: String, password: String |               | token: String                                  |
| PUT    | Registration                          | login: String, password: String |               | token: String                                  |


##### History
```
/api/history
```
| Method | Description                 | Params            | Auth required | Result |
|--------|-----------------------------|-------------------|---------------|--------|
| GET    | Get new or updated items    |  timestamp: Long  |       +       |        |
| POST   | Store new or updated mangas |                   |       +       |        |
| DELETE | Remove history items        | data: [{id: Int}] |       +       |        |