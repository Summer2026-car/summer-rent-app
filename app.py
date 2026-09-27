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

  # Lectura directa en memoria compatible con celulares
  with open(pdf_filename, "rb") as pdf_file:
    PDFbyte = pdf_file.read()

  st.download_button(
      label="📥 Descargar PDF de Cotización",
      data=PDFbyte,
      file_name=pdf_filename,
      mime="application/pdf",
  )
