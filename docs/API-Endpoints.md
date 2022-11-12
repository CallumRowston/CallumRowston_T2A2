# API Endpoints Documentaiton

## Table Of Contents

- [Auth Routes](#auth-routes)
- [Admin Routes](#admin-routes)
- [User Routes](#user-routes)
- [Canyon Routes](#canyon-routes)

### Auth Routes

#### **Route: /auth/register/**

- Request Verb: POST
- Function: Registers a new user in the database
- Required Arguments: N/A
- Authentication: N/A
- Authorization: N/A
- Example Request: 
```JSON
{
    "name": "NewCanyonUser",
    "email": "canyon@gmail.com",
    "password": "Ilikecanyons123"
}
```
- Example Response:
```JSON
{
    "id": 4,
    "name": "NewCanyonUser",
    "email": "canyon@gmail.com",
    "is_admin": false
}
```

#### **Route: /auth/login/**

- Request Verb: POST
- Function: Registered user login
- Required Arguments: N/A
- Authentication: N/A
- Authorization: N/A
- Example Request: 
```JSON
{
    "name": "CanyonAdministrator",
    "email": "canyon@admin.com",
    "password": "canyon123"
}
```
- Example Response:
```JSON
{
    "email": "canyon@admin.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODIxODUxNSwianRpIjoiZTVhMjQ3ZmQtYzY3MS00NzdkLWE0ODQtZDIyZmM2Y2I5Y2VkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE2NjgyMTg1MTUsImV4cCI6MTY2ODMwNDkxNX0.NPXiwv8tfpaeocrZoMuinryAovxZYiNCqfPSusUe3xo",
    "is_admin": true
}
```

### Admin Routes

#### **Route: /admin/grant_admin/\<int:user_id>/**

- Request Verb: PATCH
- Function: Gives admin privileges to a user
- Required Arguments: user_id
- Authentication: jwt_required
- Authorization: Admin only - get_jwt_identity
- Example Request: N/A
- Example Response:
```JSON
{
    "id": 3,
    "name": "John_Smith",
    "email": "johnsmith@canyon.com",
    "is_admin": true
}
```

#### **Route: /admin/remove_admin/\<int:user_id>/**

- Request Verb: PATCH
- Function: Removes admin privileges from a user
- Required Arguments: user_id
- Authentication: jwt_required
- Authorization: Admin only - get_jwt_identity
- Example Request: N/A
- Example Response:
```JSON
{
    "id": 3,
    "name": "John_Smith",
    "email": "johnsmith@canyon.com",
    "is_admin": false
}
```

#### **Route: /admin/delete_comment/\<int:comment_id>/**

- Request Verb: DELETE
- Function: Allows admin to delete an users' comment
- Required Arguments: comment_id
- Authentication: jwt_required
- Authorization: Admin only - get_jwt_identity
- Example Request: N/A
- Example Response:
```JSON
{
    "Message": "Comment with id: 2 successfully deleted"
}
```

### User Routes

#### **Route: /users/**

- Request Verb: GET
- Function: Returns all users
- Required Arguments: N/A
- Authentication: jwt_required
- Authorization: Admin only - get_jwt_identity
- Example Request: N/A
- Example Response:
```JSON
[
    {
        "id": 1,
        "name": "CanyonAdministrator",
        "email": "canyon@admin.com",
        "is_admin": true
    },
    {
        "id": 2,
        "name": "Callum_Rowston",
        "email": "callum_r@canyon.com",
        "is_admin": false
    },
    {
        "id": 3,
        "name": "John_Smith",
        "email": "johnsmith@canyon.com",
        "is_admin": false
    }
]
```

#### **Route: /users/\<int:id>/**

- Request Verb: GET
- Function: Returns one user
- Required Arguments: id
- Authentication: jwt_required
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
{
    "id": 2,
    "name": "Callum_Rowston",
    "is_admin": false
}
```

#### **Route: /users/update/**

- Request Verb: PUT, PATCH
- Function: Updates a user's own username, email and/or password
- Required Arguments: N/A
- Authentication: jwt_required
- Authorization: N/A
- Example Request:
```JSON
{
    "name": "CanyonAdminUpdatedName"
}
```
- Example Response:
```JSON
{
    "Message": "User successfully updated",
    "User": {
        "id": 1,
        "name": "CanyonAdminUpdatedName",
        "email": "canyon@admin.com",
        "is_admin": true
    }
}
```

### Canyon Routes

#### **Route: /canyons/**

- Request Verb: GET
- Function: Returns all canyons
- Required Arguments: N/A
- Authentication: N/A
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
[
    {
        "id": 1,
        "name": "Starlight",
        "area": "Newnes",
        "description": "Impressive canyon with long dark tunnel with glowworms and a bat colony. A very long boulder field and fire trail to hike out means it can be a very long day, so come prepared.",
        "estimated_time_hrs": 9,
        "number_abseils": 3,
        "longest_abseil": "25m",
        "difficulty": "Medium",
        "wetsuits_recommended": false,
        "last_updated": "2022-11-12",
        "user": {
            "name": "CanyonAdminUpdatedName"
        },
        "comments": [
            {
                "id": 3,
                "message": "Our group did this on 2/4/22 and finding the entrance quite difficult. ",
                "date_posted": "2022-11-12",
                "user": {
                    "name": "John_Smith"
                }
            },
            {
                "id": 4,
                "message": "When you exit the main constriction, keep as high and left as possible to avoid the boulder field until you reach the main river",
                "date_posted": "2022-11-12",
                "user": {
                    "name": "Callum_Rowston"
                }
            }
        ]
    },
    {
        "id": 2,
        "name": "Firefly",
        "area": "Newnes",
        "description": "A good canyon to the north of the Wolgan Valley with many short abseils and swims.",
        "estimated_time_hrs": 8,
        "number_abseils": 7,
        "longest_abseil": "20m",
        "difficulty": "Medium",
        "wetsuits_recommended": true,
        "last_updated": "2022-11-12",
        "user": {
            "name": "CanyonAdminUpdatedName"
        },
        "comments": [
            {
                "id": 1,
                "message": "A test comment by the CanyonAdministrator",
                "date_posted": "2022-11-12",
                "user": {
                    "name": "CanyonAdminUpdatedName"
                }
            }
        ]
    },
    {
        "id": 3,
        "name": "Rocky Creek",
        "area": "South Wolgan",
        "description": "A long, dark and spectacular canyon in the South Wolgan. A great beginner canyon as there is no abseiling required and be easily linked up with Twister Canyon to make up a full day",
        "estimated_time_hrs": 4,
        "number_abseils": 0,
        "longest_abseil": "N/A",
        "difficulty": "Easy",
        "wetsuits_recommended": true,
        "last_updated": "2022-11-12",
        "user": {
            "name": "CanyonAdminUpdatedName"
        },
        "comments": []
    },
]
```

#### **Route: /canyons/\<int:id>/**

- Request Verb: GET
- Function: Returns one canyon
- Required Arguments: id
- Authentication: N/A
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
{
    "id": 7,
    "name": "Claustral",
    "area": "Carmarthen Labyrinth",
    "description": "Likely the most impressive canyon in NSW. Three back-to-back abseils lead to a long, sustained moss-covered canyon section lasting up to 1km. A long, difficult day with lots of bouldering, abseiling, swims and a veyr long hike out",
    "estimated_time_hrs": 10,
    "number_abseils": 5,
    "longest_abseil": "20m",
    "difficulty": "Medium",
    "wetsuits_recommended": true,
    "last_updated": "2022-11-12",
    "user": {
        "name": "CanyonAdminUpdatedName"
    },
    "comments": []
}
```

#### **Route: /canyons/\<string:difficulty>/**

- Request Verb: GET
- Function: Returns all canyons of the specified difficulty
- Required Arguments: difficulty
- Authentication: N/A
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
{
    "Message": "All Easy canyons successfully found",
    "Canyon": [
        {
            "id": 3,
            "name": "Rocky Creek",
            "area": "South Wolgan",
            "description": "A long, dark and spectacular canyon in the South Wolgan. A great beginner canyon as there is no abseiling required and be easily linked up with Twister Canyon to make up a full day",
            "estimated_time_hrs": 4,
            "number_abseils": 0,
            "longest_abseil": "N/A",
            "difficulty": "Easy",
            "wetsuits_recommended": true,
            "last_updated": "2022-11-12",
            "user": {
                "name": "CanyonAdminUpdatedName"
            },
            "comments": []
        },
        {
            "id": 4,
            "name": "Twister",
            "area": "South Wolgan",
            "description": "A short canyon that runs off Rocky Creek canyon. Features many jumps and slides and no abseils, making it ideal for beginners",
            "estimated_time_hrs": 3,
            "number_abseils": 0,
            "longest_abseil": "N/A",
            "difficulty": "Easy",
            "wetsuits_recommended": true,
            "last_updated": "2022-11-12",
            "user": {
                "name": "CanyonAdminUpdatedName"
            },
            "comments": []
        }
    ]
}
```

#### **Route: /canyons/**

- Request Verb: POST
- Function: Creates a new canyon in the database
- Required Arguments: N/A
- Authentication: jwt_required
- Authorization: Admin only - get_jwt_identity
- Example Request:
```JSON
{
    "name": "Dalpura",
    "area": "North Grose",
    "description": "Short canyon on the north side of the Grose Valley with one abseil down a short overhung waterfall into a dark cave and short constriction",
    "estimated_time_hrs": 3,
    "number_abseils": 1,
    "longest_abseil": "20m",
    "difficulty": "Easy",
    "wetsuits_recommended": false
}
```
- Example Response:
```JSON
{
    "Message": "Canyon added successfully",
    "Canyon": {
        "id": 8,
        "name": "Dalpura",
        "area": "North Grose",
        "description": "Short canyon on the north side of the Grose Valley with one abseil down a short overhung waterfall into a dark cave and short constriction",
        "estimated_time_hrs": 3,
        "number_abseils": 1,
        "longest_abseil": "20m",
        "difficulty": "Easy",
        "wetsuits_recommended": false,
        "last_updated": "2022-11-12",
        "user": {
            "name": "CanyonAdminUpdatedName"
        },
        "comments": []
    }
}
```

#### **Route: /canyons/\<int:id>/update/**

- Request Verb: PUT, PATCH
- Function: Updates an existing canyon in the database
- Required Arguments: id
- Authentication: jwt_required
- Authorization: Admin only - get_jwt_identity
- Example Request:
```JSON
{
    "name": "Dalpura Creek",
    "area": "North Grose",
    "description": "Short canyon on the north side of the Grose Valley with one abseil down a short overhung waterfall into a dark cave and short constriction",
    "estimated_time_hrs": 4,
    "number_abseils": 3
}
```
- Example Response:
```JSON
{
    "Message": "Canyon updated successfully",
    "Canyon": {
        "id": 8,
        "name": "Dalpura Creek",
        "area": "North Grose",
        "description": "Short canyon on the north side of the Grose Valley with one abseil down a short overhung waterfall into a dark cave and short constriction",
        "estimated_time_hrs": 4,
        "number_abseils": 3,
        "longest_abseil": "20m",
        "difficulty": "Easy",
        "wetsuits_recommended": false,
        "last_updated": "2022-11-12",
        "user": {
            "name": "CanyonAdminUpdatedName"
        },
        "comments": []
    }
}
```

#### **Route: /canyons/\<int:id>/**

- Request Verb: DELETE
- Function: Deletes an existing canyon from the database
- Required Arguments: id
- Authentication: jwt_required
- Authorization: Admin only - get_jwt_identity
- Example Request: N/A
- Example Response:
```JSON
{
    "Message": "Canyon with id: 8 successfully deleted."
}
```

#### **Route: /canyons/\<int:id>/comments/**

- Request Verb: GET
- Function: Returns all comments belonging to canyon id
- Required Arguments: id
- Authentication: N/A
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
[
    {
        "id": 3,
        "message": "Our group did this on 2/4/22 and finding the entrance quite difficult. ",
        "date_posted": "2022-11-12",
        "user": {
            "name": "John_Smith"
        }
    },
    {
        "id": 4,
        "message": "When you exit the main constriction, keep as high and left as possible to avoid the boulder field until you reach the main river",
        "date_posted": "2022-11-12",
        "user": {
            "name": "Callum_Rowston"
        }
    }
]
```

#### **Route: /canyons/comments/\<int:comment_id>/**

- Request Verb: GET
- Function: Returns one comment
- Required Arguments: comment_id
- Authentication: N/A
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
{
    "id": 1,
    "message": "A test comment by the CanyonAdministrator",
    "date_posted": "2022-11-12",
    "user": {
        "name": "CanyonAdminUpdatedName"
    }
}
```

#### **Route: /canyons/comments/user/\<int:user_id>/**

- Request Verb: GET
- Function: Returns all comments from a user
- Required Arguments: user_id
- Authentication: N/A
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
[
    {
        "id": 3,
        "message": "Our group did this on 2/4/22 and finding the entrance quite difficult. ",
        "date_posted": "2022-11-12",
        "user": {
            "name": "John_Smith"
        }
    },
    {
        "id": 5,
        "message": "After the rain last week multiple routes are full submerged and our group found a fair bit of debris in them so opted to scramble and abseil over the top",
        "date_posted": "2022-11-12",
        "user": {
            "name": "John_Smith"
        }
    }
]
```

#### **Route: /canyons/\<int:id>/comments/**

- Request Verb: POST
- Function: Adds a comment to a selected canyon
- Required Arguments: id
- Authentication: jwt_required
- Authorization: N/A
- Example Request:
```JSON
{
    "message": "This is a comment to show an example for endpoint documentation"
}
```
- Example Response:
```JSON
{
    "Message": "Comment posted successfully",
    "Comment": {
        "id": 7,
        "message": "This is a comment to show an example for endpoint documentation",
        "date_posted": "2022-11-12",
        "user": {
            "name": "CanyonAdminUpdatedName"
        }
    }
}
```

#### **Route: /canyons/comments/\<int:comment_id>/**

- Request Verb: PUT, PATCH
- Function: Updates a selected comment if the logged in user is the owner
- Required Arguments: comment_id
- Authentication: jwt_required
- Authorization: N/A
- Example Request:
```JSON
{
    "message": "This is an updated comment"
}
```
- Example Response:
```JSON
{
    "Message": "Comment updated successfully",
    "Comment": {
        "id": 7,
        "message": "This is an updated comment",
        "date_posted": "2022-11-12",
        "user": {
            "name": "CanyonAdminUpdatedName"
        }
    }
}
```

#### **Route: /canyons/comments/\<int:comment_id>/**

- Request Verb: DELETE
- Function: Deletes a selected comment if the logged in user is the owner
- Required Arguments: comment_id
- Authentication: jwt_required
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
{
    "Message": "Comment with id: 7 successfully deleted"
}
```

#### **Route: /canyons/to_do/\<int:user_id>/**

- Request Verb: GET
- Function: Returns all UserCanyon entries and nested canyons that the specified user has tagged as 'To Do'
- Required Arguments: user_id
- Authentication: jwt_required
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
[
    {
        "id": 5,
        "date_added": "2022-11-12",
        "tag": "To Do",
        "canyon": {
            "id": 6,
            "name": "Whungee Wheengee",
            "area": "Wollangambe",
            "description": "An excellent, sustained but difficult canyon with tight constrictions, many short abseils, swims, jumps and possible duck unders in high water.",
            "estimated_time_hrs": 10,
            "number_abseils": 6,
            "longest_abseil": "15m",
            "difficulty": "Hard",
            "wetsuits_recommended": true,
            "last_updated": "2022-11-12"
        },
        "user": {
            "id": 2
        }
    }
]
```

#### **Route: /canyons/to_do/\<int:user_id>/**

- Request Verb: GET
- Function: Returns all UserCanyon entries and nested canyons that the specified user has tagged as 'Completed'
- Required Arguments: user_id
- Authentication: jwt_required
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
[
    {
        "id": 3,
        "date_added": "2022-11-12",
        "tag": "Completed",
        "canyon": {
            "id": 4,
            "name": "Twister",
            "area": "South Wolgan",
            "description": "A short canyon that runs off Rocky Creek canyon. Features many jumps and slides and no abseils, making it ideal for beginners",
            "estimated_time_hrs": 3,
            "number_abseils": 0,
            "longest_abseil": "N/A",
            "difficulty": "Easy",
            "wetsuits_recommended": true,
            "last_updated": "2022-11-12"
        },
        "user": {
            "id": 2
        }
    },
    {
        "id": 4,
        "date_added": "2022-11-12",
        "tag": "Completed",
        "canyon": {
            "id": 5,
            "name": "Tiger Snake",
            "area": "South Wolgan",
            "description": "A narrow twisting canyon with an upper and lower constriction. A usually dry canyon that makes it ideal to do in winter",
            "estimated_time_hrs": 7,
            "number_abseils": 5,
            "longest_abseil": "25m",
            "difficulty": "Medium",
            "wetsuits_recommended": false,
            "last_updated": "2022-11-12"
        },
        "user": {
            "id": 2
        }
    }
]
```

#### **Route: /canyons/to_do/\<int:id>/**

- Request Verb: POST
- Function: Adds a UserCanyon entry for the specifieed canyon and logged in user and tags it as 'To Do'
- Required Arguments: id
- Authentication: jwt_required
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
{
    "Message": "Canyon successfully added to To Do list",
    "Entry": {
        "id": 9,
        "date_added": "2022-11-12",
        "tag": "To Do",
        "canyon": {
            "id": 6,
            "name": "Whungee Wheengee",
            "area": "Wollangambe",
            "description": "An excellent, sustained but difficult canyon with tight constrictions, many short abseils, swims, jumps and possible duck unders in high water.",
            "estimated_time_hrs": 10,
            "number_abseils": 6,
            "longest_abseil": "15m",
            "difficulty": "Hard",
            "wetsuits_recommended": true,
            "last_updated": "2022-11-12"
        },
        "user": {
            "id": 1
        }
    }
}
```

#### **Route: /canyons/completed/\<int:id>/**

- Request Verb: POST
- Function: Adds a UserCanyon entry for the specifieed canyon and logged in user and tags it as 'Completed'
- Required Arguments: id
- Authentication: jwt_required
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
{
    "Message": "Canyon successfully added to Completed list",
    "Entry": {
        "id": 10,
        "date_added": "2022-11-12",
        "tag": "Completed",
        "canyon": {
            "id": 4,
            "name": "Twister",
            "area": "South Wolgan",
            "description": "A short canyon that runs off Rocky Creek canyon. Features many jumps and slides and no abseils, making it ideal for beginners",
            "estimated_time_hrs": 3,
            "number_abseils": 0,
            "longest_abseil": "N/A",
            "difficulty": "Easy",
            "wetsuits_recommended": true,
            "last_updated": "2022-11-12"
        },
        "user": {
            "id": 1
        }
    }
}
```

#### **Route: /canyons/to_do/\<int:id>/**

- Request Verb: DELETE
- Function: Deletes a UserCanyon entry for the specifieed canyon and logged in user that is tagged as 'To Do'
- Required Arguments: id
- Authentication: jwt_required
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
{
    "Message": "To Do Canyon with id: 4 successfully removed from To Do list."
}
```

#### **Route: /canyons/completed/\<int:id>/**

- Request Verb: DELETE
- Function: Deletes a UserCanyon entry for the specifieed canyon and logged in user that is tagged as 'Completed'
- Required Arguments: id
- Authentication: jwt_required
- Authorization: N/A
- Example Request: N/A
- Example Response:
```JSON
{
    "Message": "Completed Canyon with id: 4 successfully removed from Completed list."
}
```
