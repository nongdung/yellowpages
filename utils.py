def convert_mobile_number(old_phone):
    prefix_dict = {
        '0120': '070', #mobi
        '0121': '079',
        '0122': '077',
        '0126': '076',
        '0128': '078',
        '0123': '083', #vina
        '0124': '084',
        '0125': '085',
        '0127': '081',
        '0129': '082',
        '0162': '032', #viettel
        '0163': '033',
        '0164': '034',
        '0165': '035',
        '0166': '036',
        '0167': '037',
        '0168': '038',
        '0169': '039',
        '0186': '056', #vietnamobile
        '0188': '058',
        '0199': '059', #Gmobile
        '84120': '8470', #mobi
        '84121': '8479',
        '84122': '8477',
        '84126': '8476',
        '84128': '8478',
        '84123': '8483', #vina
        '84124': '8484',
        '84125': '8485',
        '84127': '8481',
        '84129': '8482',
        '84162': '8432', #viettel
        '84163': '8433',
        '84164': '8434',
        '84165': '8435',
        '84166': '8436',
        '84167': '8437',
        '84168': '8438',
        '84169': '8439',
        '84186': '8456', #vietnamobile
        '84188': '8458',
        '84199': '8459' #Gmobile
    }
    new_phone = old_phone
    length = len(old_phone)
    #print(old_phone[0:2])
    if old_phone[0:2] == '01':
        for old_prefix, new_prefix in prefix_dict.items():
            if old_phone[0:4] == old_prefix:
                new_phone = new_prefix + old_phone[4:length]
            #print('old:', old_prefix, 'new:', new_prefix)
    elif old_phone[0:2] == '84':
        for old_prefix, new_prefix in prefix_dict.items():
            if old_phone[0:5] == old_prefix:
                new_phone = new_prefix + old_phone[5:length]
    return new_phone
