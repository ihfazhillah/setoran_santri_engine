from datetime import datetime
from setoran_models import Santri, select, count, left_join, db_session

@db_session
def get_belum_setor():
    santri_day = left_join(santri for santri in Santri for setoran in santri.setorans  if setoran.timestamp.date() == datetime.now().date())

    santri = select(santri for santri in Santri if santri not in santri_day).filter(lambda s: not s.setorans)

    return santri

@db_session
def get_belum_murojaah():

    santri = left_join(santri for santri in Santri for setoran in santri.setorans if setoran.jenis != 'murojaah' or not setoran)

    result = santri.filter(lambda s: 'murojaah' not in s.setorans.jenis)

    return result

@db_session
def get_sudah_tambah_harus_ulang():
    return left_join(santri for santri in Santri \
                     for setoran in santri.setorans \
                     if setoran.jenis == 'tambah' and setoran.lulus is False)

@db_session
def get_sudah_murojaah_harus_ulang():
    return left_join(santri for santri in Santri \
                     for setoran in santri.setorans\
                     if setoran.jenis == 'murojaah' and setoran.lulus is False)

@db_session
def get_sudah_free():
    """sudah free adalah ketika jenis setoran == murojaah dan jenis murojaah == tambah dan lulus kedua duanya == True

    Trick:
        - query pertama mendapatkan santri yang jenis murojaah dan jenis adalah tambah, dan disetiap row yang didapatkan harus status dari kelulusan adalah True
        - query kedua untuk menfilter santri yang sudah memiliki 2 row dari setorans yang didapatkan dari query pertama """
    santri = left_join(santri for santri in Santri \
                     for setoran in santri.setorans \
                     if (setoran.jenis == 'murojaah' or setoran.jenis == 'tambah') and setoran.lulus is True)


    return santri.filter(lambda s: count(s.setorans) == 2)


   