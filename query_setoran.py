from setoran_models import *


def get_belum_setor():
    return select(santri for santri in Santri if not santri.setorans)

def get_belum_murojaah():

    santri = left_join(santri for santri in Santri for setoran in santri.setorans if setoran.jenis != 'murojaah' or not setoran)

    result = santri.filter(lambda s: 'murojaah' not in s.setorans.jenis)

    return result

def get_sudah_tambah_harus_ulang():
    return left_join(santri for santri in Santri \
                     for setoran in santri.setorans \
                     if setoran.jenis == 'tambah' and setoran.lulus is False)

def get_sudah_murojaah_harus_ulang():
    return left_join(santri for santri in Santri \
                     for setoran in santri.setorans\
                     if setoran.jenis == 'murojaah' and setoran.lulus is False)
    