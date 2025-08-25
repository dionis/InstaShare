# 🎓 InstaShare - Platform to manage and share documents securely and efficiently from a smartphone or the web.

## Project Description


InstaShare is a online platform for managening documents and share its. Platform's users should be able to create an account and login with a previously created account. 

Once logged in, the user should be able to upload a file that will be processed asynchronously by the backend.
Once the file has been uploaded, the user can proceed with uploading more files, review the name, status and size of previously uploaded files, or change the name of a previously uploaded file.

Uploaded files are stored in a database or a distributed file system and a service job should pick up the file from the database / DFS, compress it with ZIP and reinsert it into the database / DFS. 
Once the file has been zipped, the user of the community site can download the file. 



## Technological Stack


### Backend


- **Python** - Primary language


- **FastAPI** - Modern web framework


- **Supabase** - Relational database


- **Docker** - Containers for local deployment and development


### Frontend


- **TypeScript** - Statically typed language


- **CSS Modules** - Modular styles


- **SASS** - CSS preprocessor


### Mobile


- **Flutter**


## Architecture

```


Frontend (TypeScript)     Mobile Apps (Flutter)


        │                           │


        └─────────┬─────────────────┘


                  │


            Backend API (FastAPI)


                  │


            Database (Supabase)


```

## System Entities

### User
  - Unique ID
  - User's name and last name
  - User's email
  - User's phonenumber
  - User's responsability
  - User's created date
  - User's updated date
  - User's deleted date
### Document
  - Unique ID
  - Document's name
  - Document's size
  - Document's type
  - Document's status
  - Document's created date
  - Document's updated date
  - Document's deleted date
### Role
  - Unique ID
  - Role's name
  - Role's descriptions
### DocumentShared
  - Unique ID
  - Document's id
  - User's id
  - Document shared date
### UserRole
 - Unique ID
 - Role's ID
 - User's ID
 - Created date
### Logs
 - Unique ID
 - User's ID
 - Event name
 - Event description
 - Created date
### SheduleJobs
 - Unique ID
 - Job title
 - Job schedule cron string
 - Job schedule description
 - Last execution date
 - Next execution date

The focus is to maintain simplicity and core functionality without additional complex features.


## Error to Fix between Supabase, SQLAlchemy and Ambic

- Supabase remot sql url SQLAlguemy (Google query with VPN)
- https://supabase.com/docs/guides/database/connecting-to-postgres
- https://github.com/orgs/supabase/discussions/35895
-  