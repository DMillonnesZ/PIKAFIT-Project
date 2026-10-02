const dbName = process.env.MONGO_DB || 'pikafit';
const pikafit = db.getSiblingDB(dbName);

// 1. Usuario ADMINISTRADOR (Permisos de estructura y mantenimiento)
pikafit.createUser({
    user: process.env.ADMIN_DB_USER,
    pwd: process.env.ADMIN_DB_PASSWORD,
    roles: [
        { role: "dbAdmin", db: dbName },
        { role: "readWrite", db: dbName }
    ]
});

// 2. Usuario CLIENTE/API (Solo lectura y escritura de datos cotidianos)
pikafit.createUser({
    user: process.env.USUARIO_DB_USER,
    pwd: process.env.USUARIO_DB_PASSWORD,
    roles: [
        { role: "readWrite", db: dbName }
    ]
});
