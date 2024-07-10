# Proje Kurulumu

Bu proje için Anaconda ortamını kullanmanız gerekmektedir. Aşağıdaki adımları izleyerek projeyi çalıştırabilirsiniz:

## Adım 1: Anaconda Ortamını Aktifleştirin

Eğer Anaconda ortamınız varsa, terminalde aşağıdaki komutu yazarak ortamı aktifleştirin:

```bash
conda activate ORTAM_ADI
```
## Adım 2: Uvicorn Sunucusunu Başlatın
```bash
uvicorn main:app --host 0.0.0.0
```
