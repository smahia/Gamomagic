# Structure

- backend: Backend project. **Flask**.
- database: Script to populate the database. Contains a prefilled database and the scheme.
- frontend: Frontend project. **Angular** 16.
- docker: Contains the docker files required to build the whole thing with a single `docker-compose up` command.

# Caveats

In the `docker` folder exists the `frontend.nginx.conf` file which is needed to expose the website. **Angular** build the project, but you need a web server to serve the `index.html`, and that is what `nginx` does. **Do not touch!**.

All the projects have a `.env` file to customize. Only used for local development. When you are running the `docker compose up` command the `.env` from the root project is loaded. 

# How to run

## Production

Edit the `.env` file in the root and customize as you wish.
Review this `DATABASE_PATH_CONFIG` variable, and edit to point a folder where the database will be. **Default is in the root project**.

Review the `PUID` and `PGID`. These values should be of your user. Check it with:

```bash
id $user
```

It will report something like:

```bash
uid=1000(user) gid=1000(user) ...
```

So you need to place those values in the `.env` file.

Finally run:

```bash
docker compose up
```

## Development

Go to the project folder and check the `README.md`.