from libs.business_health import customer_diagnostic, financial_diagnostics
# Usage
pdf_path = r'C:\Users\aleja\Desktop\Data Science\GitHub\py.customer_health\dataset\financial_reports\Estado Financiero 2022.pdf'
financial_diagnostics = financial_diagnostics(pdf_path)
#data = financial_diagnostics.extract_balanced()
data = financial_diagnostics.ratios_liquidez(ratio=1)
print(type(data))
