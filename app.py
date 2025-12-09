import streamlit as st
import streamlit.components.v1 as components
import json

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="SBBF Görev Takip Sistemi",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS İLE TAM EKRAN VE MOBİL UYUM ---
st.markdown("""
<style>
    /* Kenar boşluklarını kaldırıp tam ekran yapma */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    /* Streamlit'in varsayılan footer'ını gizle */
    footer {visibility: hidden;}
    /* Iframe'in mobilde tam oturması için */
    iframe {
        width: 100% !important;
        height: 100vh !important;
    }
</style>
""", unsafe_allow_html=True)

# --- KENAR ÇUBUĞU: VERİTABANI BAĞLANTISI ---
with st.sidebar:
    st.header("☁️ Veritabanı Ayarları")
    st.info("""
    Çok kullanıcılı (ortak) kullanım için Firebase Config bilginizi buraya yapıştırın.
    Eğer boş bırakırsanız sistem **Yerel Modda (Sadece bu cihazda)** çalışır.
    """)
    
    # Kullanıcıdan Firebase Config JSON verisini alma
    firebase_config_input = st.text_area(
        "Firebase Config (JSON)",
        placeholder='{"apiKey": "...", "authDomain": "...", "projectId": "..."}',
        height=300
    )

    # Config verisini JSON formatına çevirme denemesi
    firebase_config_json = "null"
    if firebase_config_input.strip():
        try:
            # Kullanıcı JS objesi gibi yapıştırırsa diye temizlik (basitçe)
            clean_input = firebase_config_input.replace("const firebaseConfig =", "").replace(";", "").strip()
            # Eğer valid JSON ise string olarak React'e göndereceğiz
            json.loads(clean_input) # Test et
            firebase_config_json = clean_input
            st.success("Bağlantı formatı geçerli! ✅")
        except:
            st.warning("Lütfen geçerli bir JSON formatı giriniz.")

# --- REACT UYGULAMASI ---
html_code = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>SBBF Görev Sistemi</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  
  <!-- Firebase SDKs -->
  <script type="module">
    import {{ initializeApp }} from "https://www.gstatic.com/firebasejs/9.22.0/firebase-app.js";
    import {{ getFirestore, doc, onSnapshot, setDoc, getDoc }} from "https://www.gstatic.com/firebasejs/9.22.0/firebase-firestore.js";
    
    // Python'dan gelen config verisi
    window.FIREBASE_CONFIG = {firebase_config_json};
    window.initializeApp = initializeApp;
    window.getFirestore = getFirestore;
    window.doc = doc;
    window.onSnapshot = onSnapshot;
    window.setDoc = setDoc;
    window.getDoc = getDoc;
  </script>

  <style>
    body {{ background-color: #f3f4f6; overflow-x: hidden; }}
    /* Mobilde tablo kaydırma deneyimi için */
    .table-container {{
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }}
    /* Inputların ok işaretlerini gizleme (Chrome, Safari, Edge, Opera) */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {{
      -webkit-appearance: none;
      margin: 0;
    }}
    /* Inputların ok işaretlerini gizleme (Firefox) */
    input[type=number] {{
      -moz-appearance: textfield;
    }}
  </style>
</head>
<body>
  <div id="root"></div>

  <script type="text/babel">
    const {{ useState, useEffect, useMemo, useRef }} = React;

    // --- ICONS ---
    const Icon = ({{ path, className, size = 16 }}) => (
      <svg xmlns="http://www.w3.org/2000/svg" width={{size}} height={{size}} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={{className}}>
        {{path}}
      </svg>
    );

    const Icons = {{
        Save: (p) => <Icon {{...p}} path={{<><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></>}} />,
        Cloud: (p) => <Icon {{...p}} path={{<><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></>}} />,
        CloudOff: (p) => <Icon {{...p}} path={{<><path d="M22.61 16.95A5 5 0 0 0 18 10h-1.26a8 8 0 0 0-7.05-6M5 5a8 8 0 0 0 4 15h9a5 5 0 0 0 1.7-.3"/><line x1="1" y1="1" x2="23" y2="23"/></>}} />,
        Users: (p) => <Icon {{...p}} path={{<><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></>}} />,
        Calendar: (p) => <Icon {{...p}} path={{<><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></>}} />,
        Settings: (p) => <Icon {{...p}} path={{<><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></>}} />,
        Plus: (p) => <Icon {{...p}} path={{<><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></>}} />,
        Trash2: (p) => <Icon {{...p}} path={{<><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></>}} />,
        Edit: (p) => <Icon {{...p}} path={{<><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></>}} />,
        Download: (p) => <Icon {{...p}} path={{<><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></>}} />,
        UserPlus: (p) => <Icon {{...p}} path={{<><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></>}} />,
        X: (p) => <Icon {{...p}} path={{<><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></>}} />,
        ArrowDown: (p) => <Icon {{...p}} path={{<><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></>}} />,
        ArrowUp: (p) => <Icon {{...p}} path={{<><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></>}} />,
        ArrowUpDown: (p) => <Icon {{...p}} path={{<><path d="M7 15l5 5 5-5"/><path d="M7 9l5-5 5 5"/></>}} />,
        Info: (p) => <Icon {{...p}} path={{<><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></>}} />,
        RefreshCw: (p) => <Icon {{...p}} path={{<><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></>}} />,
    }};

    // --- INITIAL DATA ---
    const INITIAL_SETTINGS = [
      {{ code: 'G', label: 'Gözetmenlik', points: 1 }},
      {{ code: 'T', label: 'Tanıtım', points: 2 }},
      {{ code: 'D', label: 'Ders Verme', points: 3 }},
      {{ code: 'W', label: 'Web Koordinatör', points: 2 }},
      {{ code: 'F', label: 'Fakülte Web', points: 10 }},
      {{ code: 'P', label: 'Planlama', points: 10 }},
      {{ code: 'X', label: 'Diğer', points: 1 }},
    ];
    
    // Yüklenen dosyadan alınan veriler
    const INITIAL_PERSONNEL = [
      {{ id: 1, name: 'İhsan ÖZKOL', dept: 'Bilgi ve Belge Yönetimi', devir: 5 }},
      {{ id: 2, name: 'Talih ÖZTÜRK', dept: 'Bilgi ve Belge Yönetimi', devir: 5 }},
      {{ id: 3, name: 'Emre KARA', dept: 'Coğrafya', devir: 3 }},
      {{ id: 4, name: 'Elif DURAN', dept: 'Felsefe', devir: 3 }},
      {{ id: 5, name: 'Bulut YAVUZ', dept: 'Felsefe', devir: 0 }},
      {{ id: 6, name: 'Özlem HEPEYİLER', dept: 'İngiliz Dili ve Edebiyatı', devir: 3 }},
      {{ id: 7, name: 'Hüseyin Enes BALCI', dept: 'Medya ve İletişim', devir: 5 }},
      {{ id: 8, name: 'İsmail EROL', dept: 'Medya ve İletişim', devir: 3 }},
      {{ id: 9, name: 'Rabia SERTTAŞ', dept: 'Medya ve İletişim', devir: 5 }},
      {{ id: 10, name: 'Bükre KAHRAMANOL', dept: 'Psikoloji', devir: 4 }},
      {{ id: 11, name: 'İlkyaz KAYA YILDIRIM', dept: 'Psikoloji', devir: 5 }},
      {{ id: 12, name: 'Dilara TURGUT', dept: 'Psikoloji', devir: 4 }},
      {{ id: 13, name: 'Afife Büşra KENAR', dept: 'Sosyoloji', devir: 4 }},
      {{ id: 14, name: 'Hüseyin ÇALIŞ', dept: 'Tarih', devir: 5 }},
      {{ id: 15, name: 'Tolga AKPINAR', dept: 'Tarih', devir: 5 }},
      {{ id: 16, name: 'Asuman BAŞ', dept: 'Türk Dili ve Edebiyatı', devir: 5 }},
      {{ id: 17, name: 'Elif ŞAHİN', dept: 'Türk Dili ve Edebiyatı', devir: 5 }},
      {{ id: 18, name: 'Batuhan ERDOĞAN', dept: 'Türk Dili ve Edebiyatı', devir: 5 }},
      {{ id: 19, name: 'Nurullah KARAGÜL', dept: 'Türk Dili ve Edebiyatı', devir: 5 }},
      {{ id: 20, name: 'Fatma KARAKAYA', dept: 'Türk Dili ve Edebiyatı', devir: 3 }},
      {{ id: 21, name: 'Aslıhan BALCI', dept: 'Sanat Tarihi', devir: 3 }},
    ];

    function App() {{
      const [db, setDb] = useState(null);
      const [isOnline, setIsOnline] = useState(false);
      const [activeTab, setActiveTab] = useState('list');
      
      const [personnel, setPersonnel] = useState(INITIAL_PERSONNEL);
      const [settings, setSettings] = useState(INITIAL_SETTINGS);
      const [schedule, setSchedule] = useState([
        {{ id: 1, date: '', desc: '', assignments: {{}} }},
        {{ id: 2, date: '', desc: '', assignments: {{}} }},
        {{ id: 3, date: '', desc: '', assignments: {{}} }}
      ]);
      const [manualScores, setManualScores] = useState({{}});
      
      const [showAddPersonModal, setShowAddPersonModal] = useState(false);
      const [editingPerson, setEditingPerson] = useState(null); // Düzenlenen kişi için state
      const [newPerson, setNewPerson] = useState({{ name: '', dept: '', devir: 0 }});
      const [sortConfig, setSortConfig] = useState({{ key: null, direction: 'desc' }});

      // --- FIREBASE BAĞLANTISI ---
      useEffect(() => {{
        if (window.FIREBASE_CONFIG && window.initializeApp) {{
          try {{
            const app = window.initializeApp(window.FIREBASE_CONFIG);
            const firestore = window.getFirestore(app);
            setDb(firestore);
            setIsOnline(true);
            
            const unsub = window.onSnapshot(window.doc(firestore, "sbbf_sistem", "ana_veri"), (docSnap) => {{
              if (docSnap.exists()) {{
                const data = docSnap.data();
                if(data.personnel) setPersonnel(data.personnel);
                if(data.settings) setSettings(data.settings);
                if(data.schedule) setSchedule(data.schedule);
                if(data.manualScores) setManualScores(data.manualScores);
              }} else {{
                saveDataToCloud();
              }}
            }});
            return () => unsub();
          }} catch (e) {{
            console.error("Firebase Hatası:", e);
            setIsOnline(false);
          }}
        }} else {{
            const localP = localStorage.getItem('sbbf_personnel');
            const localSet = localStorage.getItem('sbbf_settings');
            const localSch = localStorage.getItem('sbbf_schedule');
            const localMan = localStorage.getItem('sbbf_manual');
            
            if(localP) setPersonnel(JSON.parse(localP));
            if(localSet) setSettings(JSON.parse(localSet));
            if(localSch) setSchedule(JSON.parse(localSch));
            if(localMan) setManualScores(JSON.parse(localMan));
        }}
      }}, []);

      // --- VERİ KAYDETME ---
      const saveData = (newPersonnel, newSettings, newSchedule, newManual) => {{
        if(newPersonnel) setPersonnel(newPersonnel);
        if(newSettings) setSettings(newSettings);
        if(newSchedule) setSchedule(newSchedule);
        if(newManual) setManualScores(newManual);

        const dataToSave = {{
            personnel: newPersonnel || personnel,
            settings: newSettings || settings,
            schedule: newSchedule || schedule,
            manualScores: newManual || manualScores
        }};

        if (db && isOnline) {{
             window.setDoc(window.doc(db, "sbbf_sistem", "ana_veri"), dataToSave);
        }} else {{
             if(newPersonnel) localStorage.setItem('sbbf_personnel', JSON.stringify(newPersonnel));
             if(newSettings) localStorage.setItem('sbbf_settings', JSON.stringify(newSettings));
             if(newSchedule) localStorage.setItem('sbbf_schedule', JSON.stringify(newSchedule));
             if(newManual) localStorage.setItem('sbbf_manual', JSON.stringify(newManual));
        }}
      }};
      
      const saveDataToCloud = () => {{
          if(db) window.setDoc(window.doc(db, "sbbf_sistem", "ana_veri"), {{ personnel, settings, schedule, manualScores }});
      }};

      // --- HESAPLAMA ---
      const stats = useMemo(() => {{
        const res = {{}};
        personnel.forEach(p => {{
            res[p.id] = {{ total: 0, fromSchedule: {{}}, fromManual: {{}} }};
            settings.forEach(s => {{
                res[p.id].fromSchedule[s.code] = 0;
                res[p.id].fromManual[s.code] = (manualScores[p.id] && manualScores[p.id][s.code]) || 0;
            }});
        }});

        schedule.forEach(row => {{
            Object.entries(row.assignments).forEach(([pid, val]) => {{
                if(!res[pid] || !val) return;
                const clean = val.toUpperCase();
                settings.forEach(s => {{
                    const matches = clean.match(new RegExp(s.code, 'g'));
                    if(matches) {{
                        res[pid].fromSchedule[s.code] += matches.length;
                    }}
                }});
            }});
        }});

        personnel.forEach(p => {{
            let sum = 0;
            settings.forEach(s => {{
                const count = res[p.id].fromSchedule[s.code] + res[p.id].fromManual[s.code];
                sum += count * s.points;
            }});
            res[p.id].total = sum + (p.devir || 0);
        }});

        return res;
      }}, [schedule, personnel, settings, manualScores]);

      // --- SIRALAMA ---
      const sortedPersonnel = useMemo(() => {{
         let items = [...personnel];
         if (sortConfig.key === 'total') {{
             items.sort((a, b) => {{
                 const scA = stats[a.id]?.total || 0;
                 const scB = stats[b.id]?.total || 0;
                 return sortConfig.direction === 'asc' ? scA - scB : scB - scA;
             }});
         }}
         return items;
      }}, [personnel, stats, sortConfig]);

      const deptSortedPersonnel = useMemo(() => {{
          return [...personnel].sort((a,b) => a.dept.localeCompare(b.dept, 'tr') || a.name.localeCompare(b.name, 'tr'));
      }}, [personnel]);

      // --- HANDLERS ---
      const handleManualChange = (personId, code, value) => {{
          const val = parseInt(value) || 0;
          const newManual = {{ ...manualScores }};
          if(!newManual[personId]) newManual[personId] = {{}};
          newManual[personId][code] = val;
          saveData(null, null, null, newManual);
      }};

      const handleAssignmentChange = (rowId, personId, val) => {{
          const newSchedule = schedule.map(r => r.id === rowId ? {{ ...r, assignments: {{...r.assignments, [personId]: val}} }} : r);
          saveData(null, null, newSchedule, null);
      }};
      
      const handleRowInfo = (rowId, field, val) => {{
          const newSchedule = schedule.map(r => r.id === rowId ? {{ ...r, [field]: val }} : r);
          saveData(null, null, newSchedule, null);
      }};

      const addRow = () => {{
          const newId = (Math.max(...schedule.map(s=>s.id), 0) || 0) + 1;
          const newSchedule = [...schedule, {{ id: newId, date: '', desc: '', assignments: {{}} }}];
          saveData(null, null, newSchedule, null);
      }};
      
      const removeRow = (id) => {{
          saveData(null, null, schedule.filter(s=>s.id !== id), null);
      }};

      const addPerson = () => {{
          if(!newPerson.name) return;
          const newId = (Math.max(...personnel.map(p=>p.id), 0) || 0) + 1;
          const newPersonnel = [...personnel, {{...newPerson, id: newId}}];
          saveData(newPersonnel, null, null, null);
          setShowAddPersonModal(false);
          setNewPerson({{name:'', dept:'', devir:0}});
      }};

      // Personel Güncelleme Fonksiyonu
      const handleUpdatePerson = () => {{
          if (!editingPerson || !editingPerson.name) return;
          const newPersonnel = personnel.map(p => p.id === editingPerson.id ? editingPerson : p);
          saveData(newPersonnel, null, null, null);
          setEditingPerson(null);
      }};
      
      const removePerson = (id) => {{
          if(confirm('Silmek istediğinize emin misiniz?')) {{
              saveData(personnel.filter(p=>p.id !== id), null, null, null);
          }}
      }};

      const exportCSV = (type) => {{
          let csv = "\\uFEFF";
          if(type === 'list') {{
              csv += "Sıra,Adı,Bölüm,Devir," + settings.map(s => s.label).join(",") + ",TOPLAM\\n";
              sortedPersonnel.forEach((p, i) => {{
                  const st = stats[p.id];
                  const counts = settings.map(s => st.fromSchedule[s.code] + st.fromManual[s.code]).join(",");
                  csv += `${{i+1}},"${{p.name}}","${{p.dept}}",${{p.devir}},${{counts}},${{st.total}}\\n`;
              }});
          }} else {{
              csv += "Tarih,Açıklama," + deptSortedPersonnel.map(p=>`"${{p.name}}"`).join(",") + "\\n";
              schedule.forEach(r => {{
                  csv += `"${{r.date}}","${{r.desc}}",` + deptSortedPersonnel.map(p=>`"${{r.assignments[p.id]||''}}"`).join(",") + "\\n";
              }});
          }}
          const link = document.createElement("a");
          link.href = URL.createObjectURL(new Blob([csv], {{type: "text/csv;charset=utf-8"}}));
          link.download = "SBBF_Veri.csv";
          link.click();
      }};

      return (
        <div className="min-h-screen flex flex-col font-sans text-sm text-gray-800">
          
          {{/* MODAL: YENİ EKLE */}}
          {{showAddPersonModal && (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm">
                <div className="bg-white rounded-xl shadow-2xl w-full max-w-sm overflow-hidden animate-[fadeIn_0.2s_ease-out]">
                    <div className="bg-blue-900 text-white p-4 flex justify-between items-center">
                        <h3 className="font-bold">Yeni Personel</h3>
                        <button onClick={{()=>setShowAddPersonModal(false)}}><Icons.X/></button>
                    </div>
                    <div className="p-6 space-y-3">
                        <input className="w-full border p-2 rounded" placeholder="Ad Soyad" value={{newPerson.name}} onChange={{e=>setNewPerson({{...newPerson, name:e.target.value}})}} />
                        <input className="w-full border p-2 rounded" placeholder="Bölüm" value={{newPerson.dept}} onChange={{e=>setNewPerson({{...newPerson, dept:e.target.value}})}} />
                        <input className="w-full border p-2 rounded" type="number" placeholder="Devir Puanı" value={{newPerson.devir}} onChange={{e=>setNewPerson({{...newPerson, devir:Number(e.target.value)}})}} />
                        <button onClick={{addPerson}} className="w-full bg-blue-600 text-white p-2 rounded font-bold hover:bg-blue-700">Kaydet</button>
                    </div>
                </div>
            </div>
          )}}

          {{/* MODAL: DÜZENLE */}}
          {{editingPerson && (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm">
                <div className="bg-white rounded-xl shadow-2xl w-full max-w-sm overflow-hidden animate-[fadeIn_0.2s_ease-out]">
                    <div className="bg-blue-900 text-white p-4 flex justify-between items-center">
                        <h3 className="font-bold">Personel Düzenle</h3>
                        <button onClick={{()=>setEditingPerson(null)}}><Icons.X/></button>
                    </div>
                    <div className="p-6 space-y-3">
                        <div>
                            <label className="text-xs font-bold text-gray-500">Ad Soyad</label>
                            <input className="w-full border p-2 rounded" value={{editingPerson.name}} onChange={{e=>setEditingPerson({{...editingPerson, name:e.target.value}})}} />
                        </div>
                        <div>
                            <label className="text-xs font-bold text-gray-500">Bölüm</label>
                            <input className="w-full border p-2 rounded" value={{editingPerson.dept}} onChange={{e=>setEditingPerson({{...editingPerson, dept:e.target.value}})}} />
                        </div>
                        <div>
                            <label className="text-xs font-bold text-gray-500">Devir Puanı</label>
                            <input className="w-full border p-2 rounded" type="number" value={{editingPerson.devir}} onChange={{e=>setEditingPerson({{...editingPerson, devir:Number(e.target.value)}})}} />
                        </div>
                        <button onClick={{handleUpdatePerson}} className="w-full bg-blue-600 text-white p-2 rounded font-bold hover:bg-blue-700">Güncelle</button>
                    </div>
                </div>
            </div>
          )}}

          {{/* HEADER */}}
          <header className="bg-gradient-to-r from-blue-900 to-blue-800 text-white p-3 shadow-lg sticky top-0 z-40">
            <div className="flex flex-col md:flex-row justify-between items-center gap-3 max-w-7xl mx-auto">
                <div className="flex items-center gap-3 w-full md:w-auto">
                    <div className="bg-white/10 p-2 rounded-lg"><Icons.Calendar size={{20}}/></div>
                    <div>
                        <h1 className="text-lg font-bold leading-tight">SBBF Görev Takip</h1>
                        <div className="flex items-center gap-2 text-xs text-blue-200">
                            {{isOnline ? <span className="flex items-center gap-1 text-green-300 font-bold"><Icons.Cloud size={{12}}/> Çevrimiçi (Ortak Veri)</span> : <span className="flex items-center gap-1 text-orange-300"><Icons.CloudOff size={{12}}/> Çevrimdışı (Yerel)</span>}}
                        </div>
                    </div>
                </div>
                
                <div className="flex bg-blue-950/50 p-1 rounded-lg w-full md:w-auto overflow-x-auto">
                    <button onClick={{()=>setActiveTab('list')}} className={{`flex-1 md:flex-none px-4 py-2 rounded-md flex items-center justify-center gap-2 transition-all whitespace-nowrap ${{activeTab==='list'?'bg-white text-blue-900 font-bold shadow':'text-blue-100 hover:bg-white/10'}}`}}>
                        <Icons.Users size={{16}}/> <span className="hidden sm:inline">Personel Listesi</span><span className="sm:hidden">Liste</span>
                    </button>
                    <button onClick={{()=>setActiveTab('schedule')}} className={{`flex-1 md:flex-none px-4 py-2 rounded-md flex items-center justify-center gap-2 transition-all whitespace-nowrap ${{activeTab==='schedule'?'bg-white text-blue-900 font-bold shadow':'text-blue-100 hover:bg-white/10'}}`}}>
                        <Icons.Calendar size={{16}}/> <span className="hidden sm:inline">Görev Çizelgesi</span><span className="sm:hidden">Çizelge</span>
                    </button>
                    <button onClick={{()=>setActiveTab('settings')}} className={{`flex-1 md:flex-none px-4 py-2 rounded-md flex items-center justify-center gap-2 transition-all whitespace-nowrap ${{activeTab==='settings'?'bg-white text-blue-900 font-bold shadow':'text-blue-100 hover:bg-white/10'}}`}}>
                        <Icons.Settings size={{16}}/> <span className="hidden sm:inline">Ayarlar</span><span className="sm:hidden">Ayar</span>
                    </button>
                </div>
            </div>
          </header>

          <main className="flex-1 p-2 md:p-4 max-w-[100vw] overflow-hidden">
            
            {{/* --- TAB: PERSONEL LİSTESİ --- */}}
            {{activeTab === 'list' && (
                <div className="bg-white rounded-xl shadow border border-gray-200 flex flex-col h-[85vh]">
                    <div className="p-3 border-b flex flex-wrap justify-between items-center gap-2 bg-gray-50 rounded-t-xl">
                        <div className="flex gap-2">
                             <button onClick={{()=>setShowAddPersonModal(true)}} className="bg-blue-600 text-white px-3 py-1.5 rounded hover:bg-blue-700 text-xs font-bold flex items-center gap-1"><Icons.UserPlus size={{14}}/> Ekle</button>
                             <button onClick={{()=>exportCSV('list')}} className="bg-gray-600 text-white px-3 py-1.5 rounded hover:bg-gray-700 text-xs font-bold flex items-center gap-1"><Icons.Download size={{14}}/> Excel</button>
                        </div>
                        <div className="text-xs text-gray-500 italic"><Icons.Info size={{12}} className="inline mr-1"/>Hücrelere sayı yazarak manuel ekleme yapabilirsiniz.</div>
                    </div>
                    
                    <div className="flex-1 overflow-auto table-container">
                        <table className="w-full border-collapse min-w-[800px]">
                            <thead className="bg-gray-800 text-white sticky top-0 z-10 text-xs uppercase tracking-wider">
                                <tr>
                                    <th className="p-3 text-left w-10">#</th>
                                    <th className="p-3 text-left w-48">Personel</th>
                                    {{settings.map(s => (
                                        <th key={{s.code}} className="p-2 text-center w-20 min-w-[80px]">
                                            <div className="flex flex-col items-center">
                                                <span>{{s.label}}</span>
                                                <span className="text-[9px] opacity-60">({{s.points}}p)</span>
                                            </div>
                                        </th>
                                    ))}}
                                    <th className="p-3 text-center w-20 bg-gray-700">Devir</th>
                                    <th onClick={{()=>setSortConfig({{key:'total', direction: sortConfig.direction==='asc'?'desc':'asc'}})}} className="p-3 text-center w-24 bg-blue-900 cursor-pointer hover:bg-blue-700">
                                        TOPLAM
                                    </th>
                                    <th className="w-20 text-center">İşlem</th>
                                </tr>
                            </thead>
                            <tbody className="text-gray-700 divide-y divide-gray-100">
                                {{sortedPersonnel.map((p, idx) => {{
                                    const st = stats[p.id];
                                    return (
                                        <tr key={{p.id}} className="hover:bg-blue-50/50 transition-colors group">
                                            <td className="p-3 text-center text-gray-400 font-mono text-xs">{{idx + 1}}</td>
                                            <td className="p-3">
                                                <div className="font-bold text-gray-800">{{p.name}}</div>
                                                <div className="text-[10px] text-gray-500">{{p.dept}}</div>
                                            </td>
                                            {{settings.map(s => {{
                                                const schedCount = st.fromSchedule[s.code];
                                                const manualCount = st.fromManual[s.code];
                                                const totalCount = schedCount + manualCount;
                                                return (
                                                    <td key={{s.code}} className="p-1 border-x border-dashed border-gray-100 relative">
                                                        <div className="flex flex-col items-center justify-center h-full">
                                                            <input 
                                                                type="number"
                                                                value={{manualCount === 0 ? '' : manualCount}}
                                                                onChange={{(e) => handleManualChange(p.id, s.code, e.target.value)}}
                                                                className={{`w-full h-8 text-center bg-transparent focus:bg-white focus:ring-2 ring-blue-400 rounded outline-none font-mono font-bold ${{totalCount > 0 ? 'text-blue-700' : 'text-gray-300'}} placeholder-transparent`}}
                                                                placeholder="0"
                                                            />
                                                            <div className="text-[9px] text-gray-400 pointer-events-none absolute bottom-1">
                                                                {{schedCount > 0 && <span>Otomatik: {{schedCount}}</span>}}
                                                            </div>
                                                        </div>
                                                    </td>
                                                );
                                            }})}}
                                            <td className="p-3 text-center font-mono bg-gray-50">{{p.devir}}</td>
                                            <td className="p-3 text-center font-bold text-white bg-blue-600 text-lg shadow-inner">
                                                {{st.total}}
                                            </td>
                                            <td className="p-2 text-center flex items-center justify-center gap-2">
                                                <button onClick={{()=>setEditingPerson(p)}} className="text-gray-300 hover:text-blue-500"><Icons.Edit/></button>
                                                <button onClick={{()=>removePerson(p.id)}} className="text-gray-300 hover:text-red-500"><Icons.Trash2/></button>
                                            </td>
                                        </tr>
                                    );
                                }})}}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}}

            {{/* ... DİĞER TABLAR (GÖREV ÇİZELGESİ ve AYARLAR - Değişiklik Yok) ... */}}
            {{activeTab === 'schedule' && (
                <div className="bg-white rounded-xl shadow border border-gray-200 flex flex-col h-[85vh]">
                    <div className="p-3 border-b flex justify-between items-center bg-gray-50 rounded-t-xl">
                        <div className="flex items-center gap-2 text-xs text-gray-600">
                            <span className="hidden sm:inline">Kodlar: <b>G, T, F...</b></span>
                        </div>
                        <div className="flex gap-2">
                             <button onClick={{addRow}} className="bg-green-600 text-white px-3 py-1.5 rounded hover:bg-green-700 text-xs font-bold flex items-center gap-1"><Icons.Plus size={{14}}/> Satır</button>
                             <button onClick={{()=>exportCSV('schedule')}} className="bg-gray-600 text-white px-3 py-1.5 rounded hover:bg-gray-700 text-xs font-bold flex items-center gap-1"><Icons.Download size={{14}}/> Excel</button>
                        </div>
                    </div>

                    <div className="flex-1 overflow-auto table-container">
                        <table className="w-full border-collapse">
                            <thead className="bg-gray-100 sticky top-0 z-10 shadow-sm">
                                <tr>
                                    <th className="p-2 border w-8 text-center">#</th>
                                    <th className="p-2 border w-24 min-w-[100px] text-left text-xs font-bold">Tarih</th>
                                    <th className="p-2 border w-40 min-w-[150px] text-left text-xs font-bold">Görev</th>
                                    {{deptSortedPersonnel.map(p => (
                                        <th key={{p.id}} className="p-1 border w-12 min-w-[40px] text-center bg-blue-50/50">
                                            <div className="text-[10px] font-bold text-blue-900 truncate w-12 mx-auto" title={{p.name}}>
                                                {{p.name.split(' ').map(n=>n[0]).join('')}}
                                            </div>
                                        </th>
                                    ))}}
                                    <th className="w-8"></th>
                                </tr>
                            </thead>
                            <tbody>
                                {{schedule.map((row, i) => (
                                    <tr key={{row.id}} className="group hover:bg-blue-50">
                                        <td className="p-1 border text-center text-xs text-gray-400">{{i+1}}</td>
                                        <td className="p-1 border">
                                            <input className="w-full bg-transparent text-xs outline-none" placeholder="Tarih" value={{row.date}} onChange={{e=>handleRowInfo(row.id, 'date', e.target.value)}} />
                                        </td>
                                        <td className="p-1 border">
                                            <input className="w-full bg-transparent text-xs outline-none" placeholder="Açıklama" value={{row.desc}} onChange={{e=>handleRowInfo(row.id, 'desc', e.target.value)}} />
                                        </td>
                                        {{deptSortedPersonnel.map(p => (
                                            <td key={{p.id}} className="p-1 border text-center">
                                                <input 
                                                    className="w-full text-center text-xs uppercase font-bold outline-none bg-transparent focus:bg-yellow-100 placeholder-gray-200"
                                                    placeholder="-"
                                                    value={{row.assignments[p.id] || ''}}
                                                    onChange={{e=>handleAssignmentChange(row.id, p.id, e.target.value)}}
                                                />
                                            </td>
                                        ))}}
                                        <td className="p-1 text-center">
                                            <button onClick={{()=>removeRow(row.id)}} className="text-gray-300 hover:text-red-500 opacity-0 group-hover:opacity-100"><Icons.Trash2 size={{14}}/></button>
                                        </td>
                                    </tr>
                                ))}}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}}

            {{activeTab === 'settings' && (
                <div className="bg-white rounded-xl shadow p-6 max-w-2xl mx-auto mt-4">
                    <h2 className="text-xl font-bold mb-4 flex items-center gap-2"><Icons.Settings/> Sistem Ayarları</h2>
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-6">
                        {{settings.map(s => (
                            <div key={{s.code}} className="border p-3 rounded bg-gray-50 flex flex-col items-center">
                                <div className="text-lg font-bold text-blue-800">{{s.code}}</div>
                                <div className="text-xs text-gray-600">{{s.label}}</div>
                                <div className="text-sm font-bold text-green-600">{{s.points}} Puan</div>
                            </div>
                        ))}}
                    </div>
                    <div className="bg-yellow-50 p-4 rounded border border-yellow-200 text-sm text-yellow-800">
                        <strong>Veri Sıfırlama:</strong> Sisteme format atmak ve tüm verileri silmek için aşağıdaki butonu kullanın.
                        <button onClick={{()=>{{if(confirm('Her şey silinecek!')){{localStorage.clear(); window.location.reload();}}}}}} className="block mt-2 bg-red-100 text-red-700 px-3 py-2 rounded font-bold hover:bg-red-200">
                            ⚠ Fabrika Ayarlarına Dön
                        </button>
                    </div>
                </div>
            )}}

          </main>
        </div>
      );
    }}

    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
  </script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=True)
