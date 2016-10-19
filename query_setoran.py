from datetime import datetime
from setoran_models import Santri, select, count, left_join, db_session, Setoran, exists

@db_session
def get_belum_setor():
    
    # return select(santri for santri in Santri \
    #               for setoran in santri.setorans\
    #               if not setoran.timestamp.date() == datetime.now().date()) or \
    #         select(santri for santri in Santri if not santri.setorans)
    return select(santri for santri in Santri \
        for setoran in santri.setorans \
        if count(select(setor for setor in Setoran\
            if setor.santri == santri\
            and setor.timestamp.date() == datetime.now().date())) == 0)

@db_session
def get_belum_murojaah():

    santri = left_join(santri for santri in Santri \
                       for setoran in santri.setorans \
                       if count(select(setor for setor in Setoran \
                       if setor.santri == santri\
                       and setor.jenis == 'murojaah'\
                       and setor.timestamp.date() == datetime.now().date())) == 0 or not santri.setorans)

    return santri

@db_session
def get_belum_tambah():
    return select(santri for santri in Santri\
        for setoran in santri.setorans \
        if count(select(setor for setor in Setoran if setor.santri is santri \
        and setor.jenis is 'tambah' \
        and setor.timestamp.date() is datetime.now().date())) == 0)

@db_session
def get_sudah_tambah_harus_ulang():
    """
    yang sudah tambah harus ulang adalah, ketika dia tidak punya atribut setor.jenis is 'tambah' dan setor.lulus is True di hari ini,
    tapi dia masih memiliki atribut 'tambah'
    """
    return select(santri for santri in Santri \
                     for setoran in santri.setorans \
                     if count(select(setor for setor in Setoran \
                     if setor.santri is santri \
                     and setor.jenis is 'tambah'\
                     and setor.lulus is  True\
                     and setor.timestamp.date() is datetime.now().date())) is 0and setoran.jenis is 'tambah')

@db_session
def get_sudah_murojaah_harus_ulang():
    return select(santri for santri in Santri for setoran in santri.setorans \
        if count(select(setor for setor in Setoran\
            if setor.santri is santri \
            and setor.jenis is 'murojaah'\
            and setor.lulus is True\
            and setor.timestamp.date() is datetime.now().date())) is 0 \
        and setoran.jenis is 'murojaah')


@db_session
def get_sudah_free():
    return select(santri for santri in Santri for setoran in santri.setorans\
        if count(select(setor for setor in Setoran\
            if setor.santri is santri\
            and setor.jenis is 'tambah'\
            and setor.lulus is True)) is 1\
        and count(select(setor for setor in Setoran\
            if setor.santri is santri\
            and setor.jenis is 'murojaah'\
            and setor.lulus is True)) is 1\
        and setoran.timestamp.date() is datetime.now().date())
