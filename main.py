from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from datetime import datetime, timedelta
from keep_alive import keep_alive
from pytz import timezone
import sqlite3
import requests

session = requests.Session()
retry = Retry(connect=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def time_zone_converter(utc_datetime):
    return utc_datetime.astimezone(timezone('Turkey'))


def ist_no(il_url, ilce_url, header):
    ilMerkez_istno = {}
    ilce_istno = {}

    request1 = session.get(il_url, headers=header).json()
    for i in range(0, len(request1)):
        il = request1[i]["il"]
        merkezilce = request1[i]["ilce"]
        merkez_ist_no = (request1[i]["sondurumIstNo"],
                         request1[i]["saatlikTahminIstNo"],
                         request1[i]["gunlukTahminIstNo"])
        ilMerkez_istno.setdefault(il, {merkezilce: None})
        ilMerkez_istno[il][merkezilce] = merkez_ist_no

        request2 = session.get(ilce_url,
                               params={
                                   "il": f"{il}"
                               },
                               headers=header).json()
        for i in range(0, len(request2)):
            ilce = request2[i]["ilce"]
            istno = (request2[i]["sondurumIstNo"],
                     request2[i]["saatlikTahminIstNo"],
                     request2[i]["gunlukTahminIstNo"])
            ilce_istno.setdefault(il, {ilce: None})
            ilce_istno[il][ilce] = istno

    return ilMerkez_istno, ilce_istno


def sonDurumVeriler(il, ilce, sonDurum_istno, sonDurum):
    veriZamani = sonDurum[0]["veriZamani"]
    sicaklik = sonDurum[0]["sicaklik"]
    hadise = sonDurum[0]["hadiseKodu"]
    yagis = sonDurum[0]["yagis00Now"]
    nem = sonDurum[0]["nem"]
    ruzgarYon = sonDurum[0]["ruzgarYon"]
    ruzgarhiz = sonDurum[0]["ruzgarHiz"]
    aktuelBasinc = sonDurum[0]["aktuelBasinc"]
    denizeIndirgenmisBasinc = sonDurum[0]["denizeIndirgenmisBasinc"]

    datetime_veriZamani = time_zone_converter(
        datetime.strptime(veriZamani, "%Y-%m-%dT%H:%M:%S.%fZ"))
    tarih = format(datetime_veriZamani, "%d/%m/%Y")
    saat = format(datetime_veriZamani, "%H:%M:%S")
    return [
        il, ilce, sonDurum_istno, tarih, saat, sicaklik, hadise, yagis, nem,
        ruzgarYon, ruzgarhiz, aktuelBasinc, denizeIndirgenmisBasinc
    ]


def sonDurum(path, il, ilce, sonDurum_istno, sonDurum_url, header):
    params = {"istno": sonDurum_istno}
    sonDurum = session.get(sonDurum_url, params=params, headers=header).json()
    if sonDurum:
        sonDurumVeri = sonDurumVeriler(il, ilce, sonDurum_istno, sonDurum)

        vt = sqlite3.connect(f'{il+"_"+ilce}.db')
        im = vt.cursor()
        sonDurum_SQL = f"""CREATE TABLE IF NOT EXISTS sonDurum
        (İl, İlçe, İstasyonNumarası, Tarih, Saat, Sıcaklık, Hadise, YağışMiktarı, Nem, RüzgarYönü, RüzgarHızı, ABasınç, DİBasınç)"""
        im.execute(sonDurum_SQL)
        komut = """SELECT Tarih,Saat FROM sonDurum WHERE Tarih=? AND Saat=?"""
        sonVeriTarihSaat = im.execute(
            komut, (sonDurumVeri[3], sonDurumVeri[4])).fetchall()
        if sonVeriTarihSaat == []:
            yeniSatır = f"""INSERT INTO sonDurum VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            im.execute(yeniSatır, sonDurumVeri)
            vt.commit()
            vt.close()
            print(
                f"{il} {ilce} istasyonuna ait son durum verileri {il}_{ilce} dosyasına yazıldı."
            )


def saatlikTahminVeriler(il, ilce, saatlikTahmin_istno, saatlikTahmin, i):
    baslangicZamani = saatlikTahmin[0]["baslangicZamani"]

    tahminTarih = saatlikTahmin[0]["tahmin"][i]["tarih"]
    hadise = saatlikTahmin[0]["tahmin"][i]["hadise"]
    sicaklik = saatlikTahmin[0]["tahmin"][i]["sicaklik"]
    hissedilenSicaklik = saatlikTahmin[0]["tahmin"][i]["hissedilenSicaklik"]
    nem = saatlikTahmin[0]["tahmin"][i]["nem"]
    ruzgarYonu = saatlikTahmin[0]["tahmin"][i]["ruzgarYonu"]
    ruzgarHizi = saatlikTahmin[0]["tahmin"][i]["ruzgarHizi"]
    maxRuzgarHizi = saatlikTahmin[0]["tahmin"][i]["maksimumRuzgarHizi"]

    datetime_baslangicZamani = time_zone_converter(
        datetime.strptime(baslangicZamani, "%Y-%m-%dT%H:%M:%S.%fZ"))
    tarih = format(datetime_baslangicZamani, "%d/%m/%Y")
    saat = format(datetime_baslangicZamani, "%H:%M:%S")

    datetime_tarih = time_zone_converter(
        datetime.strptime(tahminTarih, "%Y-%m-%dT%H:%M:%S.%fZ"))
    tahminTarihi = format(datetime_tarih, "%d/%m/%Y")
    tahminBaslangicSaati = format(datetime_tarih - timedelta(hours=3),
                                  "%H:%M:%S")
    tahminBitisSaati = format(datetime_tarih, "%H:%M:%S")
    return [
        il, ilce, saatlikTahmin_istno, tarih, saat, tahminTarihi,
        tahminBaslangicSaati, tahminBitisSaati, hadise, sicaklik,
        hissedilenSicaklik, nem, ruzgarYonu, ruzgarHizi, maxRuzgarHizi
    ]


def saatlikTahmin(path, il, ilce, saatlikTahmin_istno, saatlikTahmin_url, header):
    params = {"istno": saatlikTahmin_istno}
    saatlikTahmin = session.get(saatlikTahmin_url,
                                params=params,
                                headers=header).json()
    if saatlikTahmin:
        saatlikTahminVeri = saatlikTahminVeriler(il, ilce, saatlikTahmin_istno,
                                                 saatlikTahmin, 1)

        vt = sqlite3.connect(f'{il+"_"+ilce}.db')
        im = vt.cursor()
        saatlikTahmin_SQL = f"""CREATE TABLE IF NOT EXISTS saatlikTahmin
        (İl, İlçe, İstasyonNumarası, Tarih, Saat, TahminTarihi, BaşlangıçSaati, BitişSaati, BeklenenHadise, Sıcaklık, HissedilenSıcaklık, Nem, RüzgarYönü, OrtRüzgarHızı, MaksRüzgarHızı)"""
        im.execute(saatlikTahmin_SQL)
        komut = """SELECT Tarih,Saat FROM saatlikTahmin WHERE Tarih=? AND Saat=?"""
        sonVeriTarihSaat = im.execute(
            komut, (saatlikTahminVeri[3], saatlikTahminVeri[4])).fetchall()
        if sonVeriTarihSaat == []:
            for i in range(0, len(saatlikTahmin[0]["tahmin"])):
                saatlikTahminVeri = saatlikTahminVeriler(
                    il, ilce, saatlikTahmin_istno, saatlikTahmin, i)
                yeniSatır = f"""INSERT INTO saatlikTahmin VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
                im.execute(yeniSatır, saatlikTahminVeri)
                vt.commit()
            vt.close()
            print(
                f"{il} {ilce} istasyonuna ait saatlik tahmin verileri {il}_{ilce} dosyasına yazıldı."
            )

    else:
        print("ERROR:   API cevap vermiyor!")


def günlükTahminVeriler(il, ilce, günlükTahmin_istno, günlükTahmin, i):
    tarihGun1 = günlükTahmin[0]["tarihGun1"]

    veriZamani = günlükTahmin[0][f"tarihGun{i}"]
    hadise = günlükTahmin[0][f"hadiseGun{i}"]
    minSicaklik = günlükTahmin[0][f"enDusukGun{i}"]
    maxSicaklik = günlükTahmin[0][f"enYuksekGun{i}"]
    minNem = günlükTahmin[0][f"enDusukNemGun{i}"]
    maxNem = günlükTahmin[0][f"enYuksekNemGun{i}"]
    ruzgarYonu = günlükTahmin[0][f"ruzgarYonGun{i}"]
    ruzgarHizi = günlükTahmin[0][f"ruzgarHizGun{i}"]

    datetime_veriZamani = time_zone_converter(
        datetime.strptime(veriZamani, "%Y-%m-%dT%H:%M:%S.%fZ"))
    tahminTarihi = format(datetime_veriZamani, "%d/%m/%Y")
    tahminSaati = format(datetime_veriZamani, "%H:%M:%S")

    datetime_tarihGun1 = time_zone_converter(
        datetime.strptime(tarihGun1, "%Y-%m-%dT%H:%M:%S.%fZ"))
    tarih = format(datetime_tarihGun1 - timedelta(days=1), "%d/%m/%Y")
    saat = format(datetime_tarihGun1 - timedelta(days=1), "%H:%M:%S")
    return [
        il, ilce, günlükTahmin_istno, tarih, saat, tahminTarihi, tahminSaati,
        hadise, minSicaklik, maxSicaklik, minNem, maxNem, ruzgarYonu,
        ruzgarHizi
    ]


def günlükTahmin(path, il, ilce, günlükTahmin_istno, günlükTahmin_url, header):
    params = {"istno": günlükTahmin_istno}
    günlükTahmin = session.get(günlükTahmin_url, params=params,
                               headers=header).json()
    if günlükTahmin:
        günlükTahminVeri = günlükTahminVeriler(il, ilce, günlükTahmin_istno,
                                               günlükTahmin, 1)

        vt = sqlite3.connect(f'{il+"_"+ilce}.db')
        im = vt.cursor()
        günlükTahmin_SQL = f"""CREATE TABLE IF NOT EXISTS günlükTahmin
        (İl, İlçe, İstasyonNumarası, Tarih, Saat, TahminTarihi, TahminSaati, Hadise, MinSıcaklık, MaxSıcaklık, MinNem, MaxNem, RüzgarYönü, RüzgarHızı)"""
        im.execute(günlükTahmin_SQL)
        komut = """SELECT Tarih,Saat FROM günlükTahmin WHERE Tarih=? AND Saat=?"""
        sonVeriTarihSaat = im.execute(
            komut, (günlükTahminVeri[3], günlükTahminVeri[4])).fetchall()
        if sonVeriTarihSaat == []:
            for i in [1, 2, 3, 4, 5]:
                günlükTahminVeri = günlükTahminVeriler(il, ilce,
                                                       günlükTahmin_istno,
                                                       günlükTahmin, i)
                yeniSatır = f"""INSERT INTO günlükTahmin VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
                im.execute(yeniSatır, günlükTahminVeri)
                vt.commit()
            vt.close()
            print(
                f"{il} {ilce} istasyonuna ait günlük tahmin verileri {il}_{ilce} dosyasına yazıldı."
            )

    else:
        print("ERROR:   API cevap vermiyor!")



il_url = "https://servis.mgm.gov.tr/web/merkezler/iller"
ilce_url = "https://servis.mgm.gov.tr/web/merkezler/ililcesi?"
sonDurum_url = "https://servis.mgm.gov.tr/web/sondurumlar?"
saatlikTahmin_url = "https://servis.mgm.gov.tr/web/tahminler/saatlik?"
günlükTahmin_url = "https://servis.mgm.gov.tr/web/tahminler/gunluk?"

header = {"Origin": "https://www.mgm.gov.tr/"}

istno = ist_no(il_url, ilce_url, header)
ilMerkez_istno = istno[0]
ilce_istno = istno[1]

location = {}
#-------------------------------------------------------------------------------
for il in ["Amasya", "Samsun", "Sinop", "Ordu"]:
    location.setdefault(il, ilce_istno.copy()[il])
path = "output"
#-------------------------------------------------------------------------------

while True:
    keep_alive()
    for il, ilce in location.items():
        for ilce, istno in ilce.items():
            if None not in istno:
                ilce = ilce.replace("/", "-")
                sonDurum_istno = istno[0]
                sonDurum(path, il, ilce, sonDurum_istno, sonDurum_url, header)

                saatlikTahmin_istno = istno[1]
                saatlikTahmin(path, il, ilce, saatlikTahmin_istno,
                              saatlikTahmin_url, header)

                günlükTahmin_istno = istno[2]
                günlükTahmin(path, il, ilce, günlükTahmin_istno,
                             günlükTahmin_url, header)
