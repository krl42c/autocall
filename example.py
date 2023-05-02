from autocall import call

if __name__ == '__main__':
    callset = call.create_calls('tests/mocks/general.yml') 
    call.execute(callset)
    for key,val in callset.items():
        val.save_report("reports/")
