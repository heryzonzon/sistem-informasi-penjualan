def to_rupiah(value):
    return 'Rp{:,.2f}'.format(value)

def format_datetime(value):
    return value.strftime('%d-%m-%Y %H:%M:%S')
