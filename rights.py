import PyPDF2 as pypdf

def securityDeposit(pdfobject):
    
    pdf=pypdf.PdfFileReader(pdfobject)
    text = pdf.getFormTextFields()
    
    rent = text["The tenant will pay the rent of"]
    print(rent)
    deposit = text["The tenant is required to pay a security deposit of"]
    print(deposit)
    
    try:
        if (int(rent)/2 < int(securityDeposit)):
            return "Security deposit must be lower than rent"
        else:
            return
    except TypeError:
        return "Rent and deposit data is incomplete"
