from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
from datetime import datetime

app = FastAPI()

class OfferDetails(BaseModel):
    name: str
    position: str
    company: str
    start_date: str

@app.post("/generate-offer-letter")
def generate_offer_letter(details: OfferDetails):
    try:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Draw content
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 50, f"Offer Letter")
        p.line(50, height - 55, 550, height - 55)

        content = [
            f"Date: {datetime.today().strftime('%B %d, %Y')}",
            f"",
            f"Dear {details.name},",
            f"",
            f"We are pleased to offer you the position of {details.position} at {details.company}.",
            f"Your start date will be {details.start_date}.",
            f"",
            f"We look forward to working with you.",
            f"",
            f"Best regards,",
            f"{details.company} HR Team"
        ]

        y = height - 100
        for line in content:
            p.drawString(50, y, line)
            y -= 20

        p.showPage()
        p.save()

        buffer.seek(0)
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=offer_letter_{details.name}.pdf"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
