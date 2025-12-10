# core/program_data.py

PROGRAM_DETAILS = {
    "Terapi Integrasi Sensorik": {
        "code": "C1",
        "title": "Terapi Integrasi Sensorik",
        "goal": "Membantu otak anak memproses informasi sensorik (suara, sentuhan, cahaya) dengan lebih efisien agar tidak merasa kewalahan (overwhelmed) atau kurang peka.",
        "activity": "Menggunakan alat seperti noise cancelling headphones, ruangan kedap suara untuk menenangkan anak.",
        "school": "Penyediaan Quiet Corner (pojok tenang) saat anak merasa bising. Penggunaan noise-canceling headphones saat belajar mandiri. Modifikasi lingkungan kelas dengan pencahayaan yang tidak terlalu menyilaukan."
    },
    "Pelatihan Keterampilan Sosial": {
        "code": "C2",
        "title": "Pelatihan Keterampilan Sosial",
        "goal": "Mengajarkan aturan sosial implisit yang tidak dipahami anak secara alami, seperti cara bergabung dalam permainan atau menyapa teman.",
        "activity": "Membuat narasi pendek bergambar yang menjelaskan situasi sosial tertentu (contoh: 'Apa yang harus dilakukan saat teman marah'). Program berbasis bukti yang mengajarkan etiket sosial melalui instruksi langsung dan bermain peran (role-play).",
        "school": "Peer-mediated instruction: Memasangkan anak dengan teman sebaya (neurotipikal) sebagai mentor sosial dalam tugas kelompok."
    },
    "Terapi Wicara Pragmatik": {
        "code": "C3",
        "title": "Terapi Wicara Pragmatik",
        "goal": "Melatih penggunaan bahasa dalam konteks sosial, bukan hanya pengucapan kata. Fokus pada turn-taking (giliran bicara) dan mempertahankan topik.",
        "activity": "Latihan diskusi kelompok kecil dengan aturan visual (misal: memegang 'tongkat bicara' untuk menandakan giliran). Latihan mendeteksi sarkasme atau idiom yang sering disalahartikan secara harfiah.",
        "school": "Guru menggunakan instruksi visual yang jelas untuk memberi tanda kapan murid boleh berbicara dan kapan harus menyimak."
    },
    "DIR (Floortime)": {
        "code": "C4",
        "title": "DIR (Developmental Individual-differences, & Relationship-based model)",
        "goal": "Membangun koneksi emosional dan kemampuan berpikir abstrak melalui interaksi bermain yang dipimpin oleh anak (child-led).",
        "activity": "Orang tua atau guru turun ke lantai (floor) bermain mengikuti minat anak, lalu perlahan menantang anak untuk memperluas interaksi tersebut menjadi cerita yang melibatkan emosi.",
        "school": "Menggunakan kartu bergambar wajah ekspresi emosi dan mendiskusikan: 'Mengapa anak di gambar ini menangis?' untuk melatih pengambilan perspektif."
    },
    "Metode TEACCH": {
        "code": "C5",
        "title": "Metode TEACCH",
        "goal": "Memberikan struktur visual yang sangat jelas untuk mengurangi kecemasan akan perubahan dan memanfaatkan kekuatan visual anak.",
        "activity": "Menggunakan gambar untuk menunjukkan urutan kegiatan harian sehingga anak tahu apa yang akan terjadi selanjutnya. Misalkan, seorang anak sangat terobsesi dengan kereta api, guru menggunakan kereta api sebagai sarana belajar matematika.",
        "school": "Memberikan peringatan waktu (timer) sebelum transisi antar mata pelajaran agar anak tidak kaget saat harus berganti aktivitas."
    },
    # Default for Low Risk
    "Pendampingan Reguler": {
        "code": "-",
        "title": "Pendampingan Reguler",
        "goal": "Memastikan anak dapat mengikuti kurikulum standar dengan sedikit penyesuaian.",
        "activity": "Monitoring berkala oleh guru kelas.",
        "school": "Anak mengikuti kelas reguler sepenuhnya dengan dukungan minimal."
    }
}

CRITERIA_NAMES = {
    'C1': 'Sensitivitas Sensorik',
    'C2': 'Interaksi Sosial',
    'C3': 'Penanganan Komunikasi',
    'C4': 'Empati & Imajinasi',
    'C5': 'Minat Terbatas'
}