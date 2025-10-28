# IntelliCV Platform Data Transfer & Tidy-Up Summary

## Objective
Create a unified, clean, and runnable version of the IntelliCV platform in `Full system`, moving excess/legacy files to backup and documenting all changes.

---

## Essential Platform Files/Folders (copied to `Full system`)
- `admin_portal/` (core admin features, backend integration, AI data loader, main.py, Dockerfiles, requirements, config, services, etc.)
- `user_portal_final/` (user-facing portal, backend integration, demo, pages, etc.)
- `ai_data_final/` (real CV/resume data, JSON analysis, job title database, feedback, etc.)
- `backend/`, `api/`, `services/`, `modules/`, `components/`, `utilities/`, `utils/`, `shared/`, `config/`, `data/`, `db/`, `monitoring/`, `nginx/`, `static/`, `logs/`, `docs/`, `fragments/`, `pgadmin/`, `redis/`, `.vscode/`, `__pycache__/` (all required for platform operation)
- `.gitignore`, `requirements.txt`, `Dockerfile`, `docker-compose.yml`, and related config files

---

## Files/Folders Moved to Backup (`Sandbox Backup data - old` or `back` directory)
- Old workspace files: `BACKEND-ADMIN-USER - linkup do not lose 25-10.code-workspace`, `BACKEND-ADMIN-USER - linkup do not lose.code-workspace`, `user - 25-10.code-workspace`, `user - 27-10.code-workspace`
- Legacy markdowns: `COMPLETE_SYNCHRONIZATION_REPORT.md`, `MAIN_PY_UPDATE_SUMMARY.md`, `REMOVED_PREMIUM_FEATURES_FOR_REUSE.md`, `RESUME_CHATBOT_ENHANCEMENT_COMPLETE.md`
- Any backup files with `.backup.<date>` suffix (e.g., `main.py.backup.20251015_162526`, `Dockerfile.backup.20251015_162526`, etc.)
- Redundant/legacy feature summaries, old sync reports, deprecated feature docs

---

## Rationale for Transfer
- **Essentials**: Only files/folders required for platform operation, testing, and development are kept in `Full system`.
- **Backups**: Legacy, backup, and workspace files are archived for reference but not needed for daily operation.
- **Documentation**: This markdown provides a clear record of what was moved, why, and the original purpose of each item.

---

## Next Steps
- Use `Full system` for all future development, testing, and deployment.
- Reference `Sandbox Backup data - old` or `back` directory only if legacy data or old configs are needed.
- Continue to keep the platform tidy by archiving unused files and documenting changes.

---

**Data transfer and tidy-up complete.**
