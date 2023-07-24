# CineMatrix

# API Documentation
frontend:https://cine-matrix.vercel.app/index.html
## User Management

### Retrieve all Users
- Method: GET
- Endpoint: `/api/users`
- Description: Retrieve a list of all users.

### Retrieve a Specific User
- Method: GET
- Endpoint: `/api/users/{id}`
- Description: Retrieve a specific user by ID.

### Create a New User
- Method: POST
- Endpoint: `/api/users`
- Description: Create a new user.

### Update an Existing User
- Method: PUT
- Endpoint: `/api/users/{id}`
- Description: Update an existing user by ID.

### Delete a User
- Method: DELETE
- Endpoint: `/api/users/{id}`
- Description: Delete a user by ID.

## Movie and Show Management

### Retrieve all Movies
- Method: GET
- Endpoint: `/api/movies`
- Description: Retrieve a list of all movies.

### Retrieve a Specific Movie
- Method: GET
- Endpoint: `/api/movies/{id}`
- Description: Retrieve a specific movie by ID.

### Create a New Movie
- Method: POST
- Endpoint: `/api/movies`
- Description: Create a new movie.

### Update an Existing Movie
- Method: PUT
- Endpoint: `/api/movies/{id}`
- Description: Update an existing movie by ID.

### Delete a Movie
- Method: DELETE
- Endpoint: `/api/movies/{id}`
- Description: Delete a movie by ID.

### Retrieve all Shows for a Movie
- Method: GET
- Endpoint: `/api/movies/{id}/shows`
- Description: Retrieve all shows associated with a specific movie.

### Create a New Show for a Movie
- Method: POST
- Endpoint: `/api/movies/{id}/shows`
- Description: Create a new show associated with a specific movie.

### Update an Existing Show for a Movie
- Method: PUT
- Endpoint: `/api/movies/{id}/shows/{showId}`
- Description: Update an existing show associated with a specific movie.

### Delete a Show for a Movie
- Method: DELETE
- Endpoint: `/api/movies/{id}/shows/{showId}`
- Description: Delete a show associated with a specific movie.

## Event and Participant Management

### Retrieve all Events
- Method: GET
- Endpoint: `/api/events`
- Description: Retrieve a list of all events.

### Retrieve a Specific Event
- Method: GET
- Endpoint: `/api/events/{id}`
- Description: Retrieve a specific event by ID.

### Create a New Event
- Method: POST
- Endpoint: `/api/events`
- Description: Create a new event.

### Update an Existing Event
- Method: PUT
- Endpoint: `/api/events/{id}`
- Description: Update an existing event by ID.

### Delete an Event
- Method: DELETE
- Endpoint: `/api/events/{id}`
- Description: Delete an event by ID.

### Retrieve all Participants for an Event
- Method: GET
- Endpoint: `/api/events/{id}/participants`
- Description: Retrieve all participants associated with a specific event.

### Add a Participant to an Event
- Method: POST
- Endpoint: `/api/events/{id}/participants`
- Description: Add a participant to a specific event.

### Remove a Participant from an Event
- Method: DELETE
- Endpoint: `/api/events/{id}/participants/{participantId}`
- Description: Remove a participant from a specific event.

## Show Hierarchical View

### Retrieve all Shows
- Method: GET
- Endpoint: `/api/shows`
- Description: Retrieve a list of all shows.

### Retrieve a Specific Show
- Method: GET
- Endpoint: `/api/shows/{id}`
- Description: Retrieve a specific show by ID.

### Create a New Show
- Method: POST
- Endpoint: `/api/shows`
- Description: Create a new show.

### Update an Existing Show
- Method: PUT
- Endpoint: `/api/shows/{id}`
- Description: Update an existing show by ID.

### Delete a Show
- Method: DELETE
- Endpoint: `/api/shows/{id}`

## User Listing

### Retrieve a Paginated List of Users
- Method: GET
- Endpoint: `/api/users`
- Description: Retrieve a paginated list of users.

### Retrieve a Filtered List of Users
- Method: GET
- Endpoint: `/api/users/filter?username={username}&membership={membership}&status={status}`
- Description: Retrieve a filtered list of users based on parameters like username, membership type, and status.

### Retrieve a Sorted List of Users
- Method: GET
- Endpoint: `/api/users/sort?sortBy={field}&sortOrder={order}`
- Description: Retrieve a sorted list of users based on a specific field and sort order.
