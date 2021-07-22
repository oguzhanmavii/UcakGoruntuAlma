from dronekit import  connect,VehicleMode,Command,LocationGlobalRelative,Vehicle
import time
from  pymavlink import mavutil

print("Bağlanıyor..")
baglanti_adresi="tcp:127.0.0.1:5762"
ucak = connect(baglanti_adresi,wait_ready=True,timeout=100)

def arm_ol():
    while ucak.is_armable==False:
        print("Arm olamıyor !")
        time.sleep(1)
    ucak.mode = VehicleMode("GUIDED")
    while ucak.mode == 'GUIDED':
        print("GUIDED moda geçiliyor..")
        time.sleep(1)
    print("GUIDED moda geçildi.")
    ucak.armed = True
    while ucak.armed is False:
        print("Arm için bekleniyor..")
        time.sleep(1)
    print("Arm oldu.")

def kalkis(kalkisAcisi,irtifa):
    kalkis_komutu= Command(0,0,0,3,mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,0,0,kalkisAcisi,0,0,0,0,0,irtifa)
    print("Kalkış komutu oluşturuldu")
    return  kalkis_komutu

def hedefNoktayaGidildi(enlem,boylam,irtifa):
    komut_git= Command(0,0,0,3,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0,enlem,boylam,irtifa)
    print("Hedef Noktaya gidiliyor..")
    return  komut_git

def goruntuTespiti(kameraAc,yakinlastir,odakNoktasi,goruntuAlma):
    goruntu_TespitEtme = Command(0,0,0,3,mavutil.mavlink.MAV_CMD_DO_DIGICAM_CONTROL,0,0,kameraAc,yakinlastir,0,odakNoktasi,goruntuAlma,0,0)
    print("Goruntu alma işlemi yapılıyor..")
    return goruntu_TespitEtme


def inis(enlem,boylam):
    komut_inis = Command(0,0,0,3,mavutil.mavlink.MAV_CMD_NAV_LAND,0,0,0,0,0,0,enlem,boylam,0)
    print("İniş için hazırlanıyor..")
    return  komut_inis

komut= ucak.commands
komut.download()
komut.wait_ready()
komut.clear()


komut1=kalkis(15,25)
komut2=hedefNoktayaGidildi(39.9041090,41.2364289,20)
komut3=hedefNoktayaGidildi(39.9052283,41.2366274,20)
komut4=goruntuTespiti(1,0,2,1)
komut5=hedefNoktayaGidildi(39.9049938,41.2381268,20)
komut6=inis(39.9042386,41.2371290)


komut.add(komut1)
komut.add(komut2)
komut.add(komut3)
komut.add(komut4)
komut.add(komut5)
komut.add(komut6)

ucak.flush()
ucak.mode=VehicleMode("AUTO")
arm_ol()

ucak.mode=VehicleMode("AUTO")
