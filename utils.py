import csv

def import_data(file_path):
    """
    header, times_ms, load_N, deformation_mcm = import_data(filename)
    Function import_data return data from the file: header, and three lists with times (ms), load (N) and deformation (micrometers).
    The input file must be *.sld (S-Lab. file v.2)
    Header dictionary contaims:
    str_id - id of the file format
    str_date - date
    scale_mm - scale of movement, mm
    scale_kN - scale of load, kN
    cross_section - cross-section of a specimen, mm^2
    marking - marking
    """
    f = open(file_path, 'rb')
    header = {}
    # Reading header, 120 bytes
    header['str_id'] = str(f.read(16), 'utf-8').replace('\x00', '')
    header['str_date'] = str(f.read(16), 'utf-8').replace('\x00', '')
    # Scale of movement, mm
    header['scale_mm'] = int.from_bytes(f.read(2), 'little', signed='false')
    # Scale of load, kN
    header['scale_kN'] = int.from_bytes(f.read(2), 'little', signed='false')
    # Cross-section of a specimen
    header['cross_section'] = int.from_bytes(f.read(2), 'little', signed='false')
    f.seek(6, 1)
    n_blocks = int.from_bytes(f.read(4), 'little')
    f.seek(50, 1)
    header['marking'] = str(f.read(17), 'utf-8').replace('\x00', '')
    f.seek(5, 1)
    # Reading data
    deformation_mcm = []
    load_N = []
    time_ms = []
    for i in range(n_blocks):
        deformation_mcm.append(int.from_bytes(f.read(4), 'little'))
        load_N.append(int.from_bytes(f.read(4), 'little'))
        time_ms.append(int.from_bytes(f.read(4), 'little'))
    return header, time_ms, load_N, deformation_mcm
    f.close()

def prepare_for_csv(header, time, load, deform):
    data = list()
    data.append(['Id', header['str_id']])
    data.append(['Date', header['str_date']])
    data.append(['Movement scale, mm', header['scale_mm']])
    data.append(['Load scale, kN', header['scale_kN']])
    data.append(['Specimen cross-section, mm^2', header['cross_section']])
    data.append(['Marking', header['marking']])
    data.append(['Time, ms', 'Load, N', 'Deforamtion, mcm'])
    for i in range(len(time)):
        data.append([time[i], load[i], deform[i]])
    return data

def save_to_csv(file_path, data):
    try:
        f = open(file_path, 'w', newline='')
        writer = csv.writer(f)
        writer.writerows(data)
        f.close
        return 1
    except:
        return -1