
# Inventario simple (Django)

Proyecto base con un único modelo `InventoryItem` y comando para importar desde Excel.

## Pasos para levantar

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scriptsctivate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Importar desde Excel (opcional)

Asegúrate de que el archivo tenga las columnas: `Assigned Bench`, `Type`, `Supplier`, `QTY`, `Description`, `Status`, `Comments`, `Storage Location` en el sheet `Inventory`.

```bash
python manage.py importar_inventario "./Benchs Inventory.xlsx" --sheet Inventory
```

## Rutas

- Admin: `http://127.0.0.1:8000/admin/`
- Listado simple: `http://127.0.0.1:8000/`
- Alta simple: `http://127.0.0.1:8000/new/`


