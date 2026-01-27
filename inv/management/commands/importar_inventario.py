
from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from inv.models import InventoryItem

class Command(BaseCommand):
    help = ("Importa items desde un Excel. "
            "Espere columnas: Assigned Bench, Type, Supplier, QTY, Description, Status, Comments, Storage Location")

    def add_arguments(self, parser):
        parser.add_argument("ruta_excel", type=str)
        parser.add_argument("--sheet", type=str, default="Inventory")

    def handle(self, *args, **opts):
        ruta = opts["ruta_excel"]
        sheet = opts["sheet"]
        try:
            df = pd.read_excel(ruta, sheet_name=sheet, engine="openpyxl")
        except Exception as e:
            raise CommandError(f"No pude leer el archivo/sheet: {e}")

        df.columns = [str(c).strip() for c in df.columns]

        requeridas = [
            "Assigned Bench", "Type", "Supplier", "QTY",
            "Description", "Status", "Comments", "Storage Location"
        ]
        faltantes = [c for c in requeridas if c not in df.columns]
        if faltantes:
            raise CommandError(f"Faltan columnas requeridas: {faltantes}")

        creados, actualizados = 0, 0
        for _, row in df.iterrows():
            key = {
                "description": str(row.get("Description", "")).strip() if pd.notna(row.get("Description")) else "",
                "supplier": str(row.get("Supplier", "")).strip() if pd.notna(row.get("Supplier")) else "",
                "type": str(row.get("Type", "")).strip() if pd.notna(row.get("Type")) else "",
                "assigned_bench": str(row.get("Assigned Bench", "")).strip() if pd.notna(row.get("Assigned Bench")) else "",
            }
            defaults = {
                "qty": float(row.get("QTY", 0)) if pd.notna(row.get("QTY")) else 0,
                "status": str(row.get("Status", "")).strip() if pd.notna(row.get("Status")) else "",
                "comments": str(row.get("Comments", "")).strip() if pd.notna(row.get("Comments")) else "",
                "storage_location": str(row.get("Storage Location", "")).strip() if pd.notna(row.get("Storage Location")) else "",
            }
            obj, created = InventoryItem.objects.update_or_create(**key, defaults=defaults)
            creados += int(created)
            if not created:
                actualizados += 1

        self.stdout.write(self.style.SUCCESS(
            f"Items creados: {creados}, actualizados: {actualizados}"
        ))
