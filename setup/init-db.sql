-- ==============================================================================
-- PostgreSQL Initialization Script for Conecta Nexus Microservices
-- Automatically executed by postgres docker-entrypoint-initdb.d
-- ==============================================================================

SELECT 'CREATE DATABASE db_auth'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'db_auth')\gexec

SELECT 'CREATE DATABASE db_profiles'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'db_profiles')\gexec

SELECT 'CREATE DATABASE db_challenges'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'db_challenges')\gexec

SELECT 'CREATE DATABASE db_applications'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'db_applications')\gexec

SELECT 'CREATE DATABASE db_moderation'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'db_moderation')\gexec

SELECT 'CREATE DATABASE db_notifications'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'db_notifications')\gexec
