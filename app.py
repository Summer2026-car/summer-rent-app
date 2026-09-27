from datetime import datetime
import base64
import os
import random
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit as st

st.set_page_config(
    page_title="Generador de Cotizaciones - Summer Rent a Car",
    page_icon="🚗",
    layout="centered",
)


def generar_pdf(data, filename):
  doc = canvas.Canvas(filename, pagesize=letter)
  width, height = letter

  left_margin = 50
  right_margin = width - 50

  logo_path = "logo.png"
  text_x = left_margin

  if os.path.exists(logo_path):
    try:
      doc.drawImage(
          logo_path,
          left_margin,
          height - 100,
          width=85,
          height=45,
          preserveAspectRatio=True,
      )
      text_x = left_margin + 95
    except Exception:
      text_x = left_margin

  doc.setFont("Helvetica-Bold", 13)
  doc.setFillColor(colors.HexColor("#2C3E50"))
  doc.drawString(text_x, height - 60, "SUMMER RENT A CAR")

  doc.setFont("Helvetica", 8)
  doc.setFillColor(colors.HexColor("#7F8C8D"))
  doc.drawString(text_x, height - 72, "info@rentacarsummer.com")
  doc.drawString(text_x, height - 83, "+506 64056463")
  doc.drawString(text_x, height - 94, "San José, Costa Rica")

  doc.setFont("Helvetica-Bold", 12)
  doc.setFillColor(colors.HexColor("#2C3E50"))
  doc.drawRightString(right_margin, height - 60, data["quote_no"])

  doc.setFont("Helvetica", 9)
  doc.setFillColor(colors.HexColor("#7F8C8D"))
  doc.drawRightString(right_margin, height - 74, data["issue_date"])

  doc.setStrokeColor(colors.HexColor("#BDC3C7"))
  doc.setFillColor(colors.HexColor("#F8F9F9"))
  doc.rect(left_margin, height - 150, width - 100, 38, fill=1, stroke=1)

  doc.setFont("Helvetica-Bold", 10)
  doc.setFillColor(colors.HexColor("#E74C3C"))
  doc.drawCentredString(
      width / 2.0, height - 125, "THIS IS A QUOTE - NOT A CONFIRMED RESERVATION"
  )
  doc.setFont("Helvetica", 8)
  doc.setFillColor(colors.HexColor("#555555"))
  doc.drawCentredString(
      width / 2.0,
      height - 138,
      "This is a price estimate, not a confirmed reservation. Prices are"
      " subject to availability.",
  )

  y = height - 180
  doc.setFont("Helvetica-Bold", 10)
  doc.setFillColor(colors.HexColor("#2C3E50"))
  doc.drawString(left_margin, y, "QUOTE INFORMATION")

  y -= 18
  doc.setFont("Helvetica", 9)
  doc.setFillColor(colors.HexColor("#333333"))
  doc.drawString(left_margin, y, "Status:")
  doc.drawString(left_margin + 120, y, data["status"])

  y -= 15
  doc.drawString(left_margin, y, "Payment Status:")
  doc.drawString(left_margin + 120, y, data["payment_status"])

  y -= 15
  doc.drawString(left_margin, y, "Deposit:")
  doc.drawString(left_margin + 120, y, f"${data['deposit']:.2f}")

  y -= 35
  col_width = (width - 100) / 2.0

  doc.setFillColor(colors.HexColor("#F2F4F4"))
  doc.rect(left_margin, y - 65, col_width - 10, 65, fill=1, stroke=0)
  doc.setFont("Helvetica-Bold", 9)
  doc.setFillColor(colors.HexColor("#2C3E50"))
  doc.drawString(left_margin + 10, y - 15, "PICK-UP")

  doc.setFont("Helvetica", 9)
  doc.setFillColor(colors.HexColor("#333333"))
  doc.drawString(left_margin + 10, y - 32, "Date:")
  doc.drawString(left_margin + 60, y - 32, data["pickup_date"])
  doc.drawString(left_margin + 10, y - 46, "Time:")
  doc.drawString(left_margin + 60, y - 46, data["pickup_time"])
  doc.drawString(left_margin + 10, y - 60, "Location:")
  doc.drawString(left_margin + 60, y - 60, data["pickup_location"])

  ret_x = left_margin + col_width + 10
  doc.setFillColor(colors.HexColor("#F2F4F4"))
  doc.rect(ret_x, y - 65, col_width - 10, 65, fill=1, stroke=0)
  doc.setFont("Helvetica-Bold", 9)
  doc.setFillColor(colors.HexColor("#2C3E50"))
  doc.drawString(ret_x + 10, y - 15, "RETURN")

  doc.setFont("Helvetica", 9)
  doc.setFillColor(colors.HexColor("#333333"))
  doc.drawString(ret_x + 10, y - 32, "Date:")
  doc.drawString(ret_x + 60, y - 32, data["return_date"])
  doc.drawString(ret_x + 10, y - 46, "Time:")
  doc.drawString(ret_x + 60, y - 46, data["return_time"])
  doc.drawString(ret_x + 10, y - 60, "Location:")
  doc.drawString(ret_x + 60, y - 60, data["return_location"])

  y -= 90
  doc.setFont("Helvetica-Bold", 10)
  doc.setFillColor(colors.HexColor("#2C3E50"))
  doc.drawString(
      left_margin, y, f"{data['vehicle_type']} - Vehicle to be Assigned"
  )

  y -= 15
  doc.setFont("Helvetica", 9)
  doc.setFillColor(colors.HexColor("#555555"))
  doc.drawString(left_margin, y, f"Duration: {data['rental_days']} day(s)")
  y -= 12
  doc.drawString(left_margin, y, f"Vehicle Type: {data['vehicle_type']}")
  y -= 12
  doc.drawString(
      left_margin, y, "Specific vehicle will be assigned before pickup date"
  )

  y -= 35
  doc.setFont("Helvetica-Bold", 9)
  doc.setFillColor(colors.HexColor("#2C3E50"))
  doc.drawString(left_margin, y, "INSURANCE")
  doc.drawString(left_margin + col_width, y, "AMENITIES")

  y -= 15
  doc.setFont("Helvetica-Bold", 9)
  doc.setFillColor(colors.HexColor("#333333"))
  doc.drawString(left_margin, y, data["insurance_type"])
  doc.setFont("Helvetica", 9)
  doc.drawString(left_margin + col_width, y, "No additional amenities")

  y -= 15
  doc.setFont("Helvetica", 8)
  doc.setFillColor(colors.HexColor("#555555"))
  doc.drawString(
      left_margin,
      y,
      "The rate includes: mandatory basic CDW/TPL insurance with excess, 1",
  )
  y -= 10
  doc.drawString(
      left_margin,
      y,
      "additional driver free, unlimited mileage and roadside assistance",
  )

  y -= 22
  doc.drawString(
      left_margin,
      y,
      f"In addition to the rental, a refundable security deposit of"
      f" ${data['deposit']:.2f} USD is",
  )
  y -= 10
  doc.drawString(
      left_margin, y, "required, via cash, credit or debit card via PayPal"
  )

  y -= 35
  doc.setFillColor(colors.HexColor("#EAECEE"))
  doc.rect(left_margin, y - 15, width - 100, 18, fill=1, stroke=0)
  doc.setFont("Helvetica-Bold", 9)
  doc.setFillColor(colors.HexColor("#2C3E50"))
  doc.drawString(left_margin + 5, y - 10, "Item")
  doc.drawRightString(right_margin - 5, y - 10, "Amount")

  items = [
      ("Price per day", f"${data['price_per_day']:.2f}"),
      ("Rental days", str(data["rental_days"])),
      ("Tpl included", "$0.00"),
  ]

  y -= 30
  doc.setFont("Helvetica", 9)
  for item, amount in items:
    doc.setFillColor(colors.HexColor("#333333"))
    doc.drawString(left_margin + 5, y, item)
    doc.drawRightString(right_margin - 5, y, amount)
    y -= 18

  y -= 5
  doc.setStrokeColor(colors.HexColor("#BDC3C7"))
  doc.line(left_margin, y + 12, right_margin, y + 12)

  doc.setFont("Helvetica-Bold", 10)
  doc.setFillColor(colors.HexColor("#2C3E50"))
  doc.drawString(left_margin + 5, y, "ESTIMATED TOTAL (Taxes included)")
  doc.drawRightString(
      right_margin - 5, y, f"${data['estimated_total']:.2f}"
  )

  y -= 40
  doc.setFont("Helvetica-Bold", 8)
  doc.drawString(left_margin, y, f"Required Deposit: ${data['deposit']:.2f}")

  y -= 15
  doc.setFont("Helvetica", 8)
  doc.setFillColor(colors.HexColor("#7F8C8D"))
  doc.drawString(
      left_margin,
      y,
      "Quote Validity: This quote is valid for 7 days from the date of issue."
      " Prices may change based on availability.",
  )
  y -= 12
  doc.drawString(
      left_margin,
      y,
      "Please note this quote does not guarantee vehicle availability until"
      " confirmed.",
  )

  doc.setFont("Helvetica", 8)
  doc.setFillColor(colors.HexColor("#7F8C8D"))
  doc.drawCentredString(
      width / 2.0,
      35,
      "Summer Rent a Car | Thank you for your preference | QUOTE - NOT A"
      " RESERVATION",
  )

  doc.save()


# Interfaz visual
st.title("🚗 Generador Rápido de Cotizaciones")
st.subheader("Summer Rent a Car")

with st.form("form_cotizacion"):
  col1, col2 = st.columns(2)
  with col1:
    fecha_inicio = st.date_input("Fecha de inicio", datetime.now().date())
    hora_inicio = st.text_input("Hora de recogida", "09:00 AM")
    lugar_inicio = st.selectbox(
        "Lugar de recogida", ["Airport", "Office", "Hotel", "Delivery"]
    )
    tipo_vehiculo = st.text_input("Tipo de vehículo", "SUV 4x4 Automatic")
    precio_por_dia = st.number_input(
        "Precio por día ($)", min_value=0.0, value=60.0, step=5.0
    )
  with col2:
    fecha_regreso = st.date_input("Fecha de regreso", datetime.now().date())
    hora_regreso = st.text_input("Hora de devolución", "09:00 AM")
    lugar_regreso = st.selectbox(
        "Lugar de devolución", ["Office", "Airport", "Hotel", "Delivery"]
    )
    tipo_seguro = st.text_input("Tipo de seguro", "Tpl")
    deposito = st.number_input(
        "Depósito de garantía ($)", min_value=0.0, value=500.0, step=50.0
    )

  submitted = st.form_submit_button("Generar Cotización en PDF con Logo")

if submitted:
  dias = (fecha_regreso - fecha_inicio).days
  if dias <= 0:
    dias = 1
  total = dias * precio_por_dia
  quote_num = f"Q-{random.randint(10000, 99999)}"
  issue_date_str = datetime.now().strftime("%d/%m/%Y 00:00")
  data = {
      "quote_no": quote_num,
      "issue_date": issue_date_str,
      "status": "Quote",
      "payment_status": "Pending",
      "deposit": deposito,
      "pickup_date": fecha_inicio.strftime("%d/%m/%Y"),
      "pickup_time": hora_inicio,
      "pickup_location": lugar_inicio,
      "return_date": fecha_regreso.strftime("%d/%m/%Y"),
      "return_time": hora_regreso,
      "return_location": lugar_regreso,
      "vehicle_type": tipo_vehiculo,
      "rental_days": dias,
      "insurance_type": tipo_seguro,
      "price_per_day": precio_por_dia,
      "estimated_total": total,
  }

  pdf_filename = f"{quote_num}.pdf"
  generar_pdf(data, pdf_filename)

  st.success(
      f"¡Cotización **{quote_num}** generada con éxito! (Días: {dias}, Total:"
      f" ${total:.2f})"
  )

  with open(pdf_filename, "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode("utf-8")

  pdf_display = (
      f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%">'
      ' height="600" type="application/pdf"></iframe>'
  )
  st.markdown(pdf_display, unsafe_allow.html=True)

  with open(pdf_filename, "rb") as pdf_file:
    st.download_button(
        label="📥 Descargar Archivo PDF",
        data=pdf_file.read(),
        file_name=pdf_filename,
        mime="application/pdf",
    )
