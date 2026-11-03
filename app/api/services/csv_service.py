import io
import asyncio
import csv
from app.models.statistic_users import StatisticUserMapped
from app.models.model import CSVResult


async def csv_process_service(records: StatisticUserMapped, email_user: str) -> CSVResult | None:
    try:
        output = io.StringIO()
        writer = csv.writer(output, delimiter=";")  # Punto e virgola per Excel Europa

        # Scriviamo l'intestazione (Header del CSV)
        writer.writerow(
            [
                "Data Snapshot",
                "Nome",
                "Email",
                "Peso",
                "Altezza",
                "Età",
                "Attività",
                "BMR",
                "Media Peso",
                "Media Altezza",
                "Media Età",
                "Media BMR",
            ]
        )

        for record in records:
            # Iteriamo sugli indici della lista interna di ogni singolo record
            for i in range(len(record.list_order)):
                writer.writerow(
                    [
                        str(record.creations_date),
                        record.name,
                        record.email,
                        record.list_weight[i] if i < len(record.list_weight) else "",
                        record.list_height[i] if i < len(record.list_height) else "",
                        record.list_age[i] if i < len(record.list_age) else "",
                        (
                            record.list_activity[i]
                            if i < len(record.list_activity)
                            else ""
                        ),
                        record.list_bmr[i] if i < len(record.list_bmr) else "",
                        record.average_weight,
                        record.average_height,
                        record.average_age,
                        record.average_bmr,
                    ]
                )

        # Riportiamo il puntatore dello stream all'inizio
        output.seek(0)

        # Restituiamo lo stream come file CSV scaricabile
        filename = (
            f"statistiche_storico_{email_user.replace('@', '_').replace('.', '_')}.csv"
        )
        
        safe_email = email_user.replace('@', '_').replace('.', '_')
        filename = f"statistiche_storico_{safe_email}.csv"

        return CSVResult(filename=filename, output=output)

    except Exception as e:
        return None
