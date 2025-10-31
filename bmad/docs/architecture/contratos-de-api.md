# Contratos de API
| Endpoint | Metodo | Request | Response |
| -------- | ------ | ------- | -------- |
| /api/projects | POST | {name} | {status,data:{project}} |
| /api/projects/{id} | GET | - | {status,data:{project,uploads,manuals}} |
| /api/projects/{id}/uploads | POST (multipart) | arquivo + metadados | {status,data:{upload_id}} |
| /api/projects/{id}/messages | POST | {message, context} | {status,data:{message_id}} (dispara workflow) |
| /api/projects/{id}/stream | GET (SSE) | - | eventos progress.update, manual.ready |
| /api/manuals/{manual_id} | GET | - | download .docx |
Erros seguem {status:"error", errors:[{code,message,hint}]}.