import streamlit as st
import streamlit.components.v1 as components

# Sayfa Ayarları (Streamlit'in ilk komutu olmalı)
st.set_page_config(
    page_title="SBBF Görev Takip Sistemi",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Kenar Çubuğu Bilgilendirmesi
with st.sidebar:
    st.info("""
    ### ℹ️ Bilgilendirme
    Bu uygulama tarayıcınızın **Yerel Depolama (LocalStorage)** özelliğini kullanır.
    
    **Veri Güvenliği:**
    - Verileriniz sadece sizin tarayıcınızda saklanır.
    - Sayfayı yenileseniz veya kapatsanız bile silinmez.
    - Verileri sıfırlamak isterseniz 'Ayarlar' sekmesindeki 'Sıfırla' butonunu kullanabilirsiniz.
    """)

# React Uygulamasının Gömülü HTML Kodu
# Not: Streamlit Cloud üzerinde sorunsuz çalışması için tüm CSS ve JS kütüphaneleri CDN üzerinden çekilmektedir.
html_code = """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SBBF Görev Sistemi</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>
    /* Streamlit iframe uyumluluğu ve kaydırma çubuğu ayarları */
    body { background-color: #f9fafb; overflow-y: auto; }
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #f1f1f1; }
    ::-webkit-scrollbar-thumb { background: #c1c1c1; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #a8a8a8; }
  </style>
</head>
<body>
  <div id="root"></div>

  <script type="text/babel">
    const { useState, useEffect, useMemo } = React;

    // --- ICON BİLEŞENLERİ (SVG) ---
    // Lucide ikonlarını React component olarak tanımlıyoruz
    const Icon = ({ path, className, size = 16, fill="none", stroke="currentColor" }) => (
      <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        {path}
      </svg>
    );

    const Icons = {
      Calendar: (props) => <Icon {...props} path={<><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></>} />,
      Users: (props) => <Icon {...props} path={<><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></>} />,
      Settings: (props) => <Icon {...props} path={<><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></>} />,
      Save: (props) => <Icon {...props} path={<><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></>} />,
      Download: (props) => <Icon {...props} path={<><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></>} />,
      Plus: (props) => <Icon {...props} path={<><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></>} />,
      Trash2: (props) => <Icon {...props} path={<><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></>} />,
      Info: (props) => <Icon {...props} path={<><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></>} />,
      UserPlus: (props) => <Icon {...props} path={<><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="20" y1="8" x2="20" y2="14"></line><line x1="23" y1="11" x2="17" y2="11"></line></>} />,
      X: (props) => <Icon {...props} path={<><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></>} />,
      ArrowDown: (props) => <Icon {...props} path={<><line x1="12" y1="5" x2="12" y2="19"></line><polyline points="19 12 12 19 5 12"></polyline></>} />,
      ArrowUp: (props) => <Icon {...props} path={<><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></>} />,
      ArrowUpDown: (props) => <Icon {...props} path={<><path d="M7 15l5 5 5-5"></path><path d="M7 9l5-5 5 5"></path></>} />,
      RefreshCw: (props) => <Icon {...props} path={<><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></>} />,
    };

    // --- BAŞLANGIÇ VERİLERİ ---
    const INITIAL_SETTINGS = [
      { code: 'G', label: 'Gözetmenlik', points: 1 },
      { code: 'T', label: 'Tanıtım', points: 2 },
      { code: 'D', label: 'Ders Verme', points: 3 },
      { code: 'W', label: 'Web Koordinatör', points: 2 },
      { code: 'F', label: 'Fakülte Web', points: 10 },
      { code: 'P', label: 'Planlama', points: 10 },
      { code: 'X', label: 'Diğer', points: 1 },
    ];

    const INITIAL_PERSONNEL = [
      { id: 1, name: 'İhsan ÖZKOL', dept: 'Bilgi ve Belge Yönetimi', devir: 5 },
      { id: 2, name: 'Talih ÖZTÜRK', dept: 'Bilgi ve Belge Yönetimi', devir: 5 },
      { id: 3, name: 'Emre KARA', dept: 'Coğrafya', devir: 3 },
      { id: 4, name: 'Elif DURAN', dept: 'Felsefe', devir: 3 },
      { id: 5, name: 'Bulut YAVUZ', dept: 'Felsefe', devir: 0 },
      { id: 6, name: 'Özlem HEPEYİLER', dept: 'İngiliz Dili ve Edebiyatı', devir: 3 },
      { id: 7, name: 'Hüseyin Enes BALCI', dept: 'Medya ve İletişim', devir: 5 },
      { id: 8, name: 'İsmail EROL', dept: 'Medya ve İletişim', devir: 3 },
      { id: 9, name: 'Rabia SERTTAŞ', dept: 'Medya ve İletişim', devir: 5 },
      { id: 10, name: 'Bükre KAHRAMANOL', dept: 'Psikoloji', devir: 4 },
      { id: 11, name: 'İlkyaz KAYA YILDIRIM', dept: 'Psikoloji', devir: 5 },
      { id: 12, name: 'Dilara TURGUT', dept: 'Psikoloji', devir: 4 },
      { id: 13, name: 'Afife Büşra KENAR', dept: 'Sosyoloji', devir: 4 },
      { id: 14, name: 'Hüseyin ÇALIŞ', dept: 'Tarih', devir: 5 },
      { id: 15, name: 'Tolga AKPINAR', dept: 'Tarih', devir: 5 },
      { id: 16, name: 'Asuman BAŞ', dept: 'Türk Dili ve Edebiyatı', devir: 5 },
      { id: 17, name: 'Elif ŞAHİN', dept: 'Türk Dili ve Edebiyatı', devir: 5 },
      { id: 18, name: 'Batuhan ERDOĞAN', dept: 'Türk Dili ve Edebiyatı', devir: 5 },
      { id: 19, name: 'Nurullah KARAGÜL', dept: 'Türk Dili ve Edebiyatı', devir: 5 },
      { id: 20, name: 'Fatma KARAKAYA', dept: 'Türk Dili ve Edebiyatı', devir: 3 },
      { id: 21, name: 'Aslıhan BALCI', dept: 'Sanat Tarihi', devir: 3 },
    ];

    const INITIAL_SCHEDULE = [
      { id: 1, date: '', desc: '', assignments: {} },
      { id: 2, date: '', desc: '', assignments: {} },
      { id: 3, date: '', desc: '', assignments: {} },
      { id: 4, date: '', desc: '', assignments: {} },
      { id: 5, date: '', desc: '', assignments: {} },
    ];

    // LocalStorage'dan güvenli veri okuma
    const loadState = (key, fallback) => {
      try {
        const stored = localStorage.getItem(key);
        return stored ? JSON.parse(stored) : fallback;
      } catch (e) {
        return fallback;
      }
    };

    function App() {
      const [activeTab, setActiveTab] = useState('schedule');
      const [personnel, setPersonnel] = useState(() => loadState('sbbf_personnel', INITIAL_PERSONNEL));
      const [settings, setSettings] = useState(() => loadState('sbbf_settings', INITIAL_SETTINGS));
      const [schedule, setSchedule] = useState(() => loadState('sbbf_schedule', INITIAL_SCHEDULE));
      
      const [showAddPersonModal, setShowAddPersonModal] = useState(false);
      const [newPerson, setNewPerson] = useState({ name: '', dept: '', devir: 0 });
      const [sortConfig, setSortConfig] = useState({ key: null, direction: 'desc' });

      // Veri değişikliklerini anlık olarak kaydet
      useEffect(() => { localStorage.setItem('sbbf_personnel', JSON.stringify(personnel)); }, [personnel]);
      useEffect(() => { localStorage.setItem('sbbf_settings', JSON.stringify(settings)); }, [settings]);
      useEffect(() => { localStorage.setItem('sbbf_schedule', JSON.stringify(schedule)); }, [schedule]);

      // Hesaplama Motoru
      const calculatedStats = useMemo(() => {
        const stats = {};
        personnel.forEach(p => {
          stats[p.id] = { totalScore: 0, counts: {} };
          settings.forEach(s => stats[p.id].counts[s.code] = 0);
        });

        schedule.forEach(row => {
          Object.entries(row.assignments).forEach(([personId, codeString]) => {
            if (!stats[personId] || !codeString) return;
            const cleanCodes = codeString.toUpperCase();
            settings.forEach(setting => {
              const regex = new RegExp(setting.code, 'g');
              const match = cleanCodes.match(regex);
              if (match) {
                const count = match.length;
                stats[personId].counts[setting.code] += count;
                stats[personId].totalScore += count * setting.points;
              }
            });
          });
        });
        return stats;
      }, [schedule, personnel, settings]);

      // Görev Çizelgesi Sıralaması (Bölüm + İsim)
      const departmentSortedPersonnel = useMemo(() => {
        return [...personnel].sort((a, b) => {
          const deptCompare = a.dept.localeCompare(b.dept, 'tr');
          if (deptCompare !== 0) return deptCompare;
          return a.name.localeCompare(b.name, 'tr');
        });
      }, [personnel]);

      // Personel Listesi Sıralaması (Puan)
      const sortedPersonnelList = useMemo(() => {
        let sortableItems = [...personnel];
        if (sortConfig.key === 'totalScore') {
          sortableItems.sort((a, b) => {
            const scoreA = (calculatedStats[a.id]?.totalScore || 0) + (a.devir || 0);
            const scoreB = (calculatedStats[b.id]?.totalScore || 0) + (b.devir || 0);
            if (scoreA < scoreB) return sortConfig.direction === 'asc' ? -1 : 1;
            if (scoreA > scoreB) return sortConfig.direction === 'asc' ? 1 : -1;
            return 0;
          });
        }
        return sortableItems;
      }, [personnel, calculatedStats, sortConfig]);

      const requestSort = (key) => {
        let direction = 'desc';
        if (sortConfig.key === key && sortConfig.direction === 'desc') direction = 'asc';
        setSortConfig({ key, direction });
      };

      const resetData = () => {
        if (window.confirm("DİKKAT! Tüm verileriniz silinecek ve başlangıç ayarlarına dönülecektir. Bu işlem geri alınamaz. Onaylıyor musunuz?")) {
          setPersonnel(INITIAL_PERSONNEL);
          setSettings(INITIAL_SETTINGS);
          setSchedule(INITIAL_SCHEDULE);
          localStorage.clear();
          window.location.reload();
        }
      };

      const handleAssignmentChange = (rowId, personId, value) => {
        setSchedule(prev => prev.map(row => row.id === rowId ? { ...row, assignments: { ...row.assignments, [personId]: value } } : row));
      };

      const handleRowInfoChange = (rowId, field, value) => {
        setSchedule(prev => prev.map(row => row.id === rowId ? { ...row, [field]: value } : row));
      };

      const addRow = () => {
        const newId = Math.max(...schedule.map(s => s.id), 0) + 1;
        setSchedule([...schedule, { id: newId, date: '', desc: '', assignments: {} }]);
      };

      const removeRow = (id) => {
        setSchedule(schedule.filter(s => s.id !== id));
      };

      const handleAddPerson = () => {
        if (!newPerson.name) return;
        const newId = Math.max(...personnel.map(p => p.id), 0) + 1;
        setPersonnel([...personnel, { ...newPerson, id: newId }]);
        setNewPerson({ name: '', dept: '', devir: 0 });
        setShowAddPersonModal(false);
      };

      const handleRemovePerson = (id) => {
        if (window.confirm("Bu personeli listeden silmek istediğinize emin misiniz?")) {
          setPersonnel(personnel.filter(p => p.id !== id));
        }
      };

      const exportToCSV = (type) => {
        let content = "";
        if (type === 'list') {
          content = "Sıra,Adı Soyadı,Bölüm,Devir Puanı," + settings.map(s => `${s.label} (${s.code})`).join(",") + ",TOPLAM PUAN\\n";
          sortedPersonnelList.forEach((p, index) => {
            const pStats = calculatedStats[p.id];
            const scores = settings.map(s => pStats.counts[s.code] || 0).join(",");
            const total = (pStats.totalScore || 0) + (p.devir || 0);
            content += `${index + 1},"${p.name}","${p.dept}",${p.devir},${scores},${total}\\n`;
          });
        } else {
          content = "Tarih,Görev Açıklaması," + departmentSortedPersonnel.map(p => `"${p.name} (${p.dept})"`).join(",") + "\\n";
          schedule.forEach(row => {
            const assignments = departmentSortedPersonnel.map(p => `"${row.assignments[p.id] || ''}"`).join(",");
            content += `"${row.date || ''}","${row.desc || ''}",${assignments}\\n`;
          });
        }

        const blob = new Blob(["\\uFEFF" + content], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `SBBF_${type === 'list' ? 'Personel_Listesi' : 'Gorev_Cizelgesi'}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      };

      return (
        <div className="min-h-screen bg-gray-50 flex flex-col font-sans text-sm relative">
          
          {showAddPersonModal && (
            <div className="fixed inset-0 bg-black/50 z-[100] flex items-center justify-center p-4">
              <div className="bg-white rounded-lg shadow-xl w-full max-w-md overflow-hidden">
                <div className="bg-blue-800 text-white p-4 flex justify-between items-center">
                  <h3 className="font-bold flex items-center gap-2"><Icons.UserPlus size={20}/> Yeni Personel Ekle</h3>
                  <button onClick={() => setShowAddPersonModal(false)} className="hover:bg-blue-700 p-1 rounded"><Icons.X size={20}/></button>
                </div>
                <div className="p-6 space-y-4">
                  <div>
                    <label className="block text-gray-700 text-xs font-bold mb-1">Adı Soyadı</label>
                    <input 
                      autoFocus
                      type="text" 
                      className="w-full border border-gray-300 rounded p-2 focus:ring-2 ring-blue-500 outline-none"
                      value={newPerson.name}
                      onChange={e => setNewPerson({...newPerson, name: e.target.value})}
                      placeholder="Örn: Ahmet Yılmaz"
                    />
                  </div>
                  <div>
                    <label className="block text-gray-700 text-xs font-bold mb-1">Bölüm</label>
                    <input 
                      type="text" 
                      className="w-full border border-gray-300 rounded p-2 focus:ring-2 ring-blue-500 outline-none"
                      value={newPerson.dept}
                      onChange={e => setNewPerson({...newPerson, dept: e.target.value})}
                      placeholder="Örn: Sosyoloji"
                    />
                  </div>
                  <div>
                    <label className="block text-gray-700 text-xs font-bold mb-1">Devir Puanı</label>
                    <input 
                      type="number" 
                      className="w-full border border-gray-300 rounded p-2 focus:ring-2 ring-blue-500 outline-none"
                      value={newPerson.devir}
                      onChange={e => setNewPerson({...newPerson, devir: Number(e.target.value)})}
                    />
                  </div>
                </div>
                <div className="p-4 bg-gray-50 flex justify-end gap-2 border-t">
                  <button onClick={() => setShowAddPersonModal(false)} className="px-4 py-2 text-gray-600 hover:bg-gray-200 rounded font-medium">İptal</button>
                  <button onClick={handleAddPerson} className="px-4 py-2 bg-blue-600 text-white rounded font-medium hover:bg-blue-700 disabled:opacity-50" disabled={!newPerson.name}>Ekle</button>
                </div>
              </div>
            </div>
          )}

          <header className="bg-blue-800 text-white p-4 shadow-lg flex justify-between items-center sticky top-0 z-50">
            <div className="flex items-center gap-3">
              <div className="bg-white/10 p-2 rounded-lg">
                <Icons.Calendar className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-xl font-bold">SBBF Görev Yönetim Sistemi</h1>
                <p className="text-blue-200 text-xs flex items-center gap-1">
                  <Icons.Save size={10} className="text-green-300"/> Otomatik Kayıt Açık
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <button 
                onClick={() => setActiveTab('schedule')}
                className={`px-4 py-2 rounded-lg transition-colors flex items-center gap-2 ${activeTab === 'schedule' ? 'bg-white text-blue-900 font-bold' : 'hover:bg-blue-700'}`}
              >
                <Icons.Calendar size={16} /> Görev Çizelgesi
              </button>
              <button 
                onClick={() => setActiveTab('list')}
                className={`px-4 py-2 rounded-lg transition-colors flex items-center gap-2 ${activeTab === 'list' ? 'bg-white text-blue-900 font-bold' : 'hover:bg-blue-700'}`}
              >
                <Icons.Users size={16} /> Personel Listesi
              </button>
              <button 
                onClick={() => setActiveTab('settings')}
                className={`px-4 py-2 rounded-lg transition-colors flex items-center gap-2 ${activeTab === 'settings' ? 'bg-white text-blue-900 font-bold' : 'hover:bg-blue-700'}`}
              >
                <Icons.Settings size={16} /> Ayarlar
              </button>
            </div>
          </header>

          <main className="flex-1 p-4 overflow-hidden flex flex-col">
            
            {activeTab === 'schedule' && (
              <div className="flex flex-col h-full bg-white rounded-lg shadow border border-gray-200">
                <div className="p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Icons.Info size={16} />
                    <span className="text-xs">Personeller <b>Bölüm</b> sırasına göre dizilmiştir. Çoklu giriş için: <b>G,T</b></span>
                  </div>
                  <div className="flex gap-2">
                    <button onClick={addRow} className="px-3 py-1.5 bg-green-600 text-white rounded hover:bg-green-700 flex items-center gap-1 text-xs">
                      <Icons.Plus size={14} /> Satır Ekle
                    </button>
                    <button onClick={() => exportToCSV('schedule')} className="px-3 py-1.5 bg-gray-600 text-white rounded hover:bg-gray-700 flex items-center gap-1 text-xs">
                      <Icons.Download size={14} /> Çizelgeyi İndir (Excel)
                    </button>
                  </div>
                </div>
                
                <div className="flex-1 overflow-auto">
                  <table className="w-full border-collapse">
                    <thead className="bg-gray-100 sticky top-0 z-20 shadow-sm">
                      <tr>
                        <th className="p-2 border border-gray-300 w-10 text-center text-gray-500">#</th>
                        <th className="p-2 border border-gray-300 w-32 text-left text-xs font-semibold text-gray-700">Tarih</th>
                        <th className="p-2 border border-gray-300 w-48 text-left text-xs font-semibold text-gray-700">Görev Açıklaması</th>
                        
                        {departmentSortedPersonnel.map(p => (
                          <th key={p.id} className="p-2 border border-gray-300 w-24 min-w-[100px] text-center text-xs font-bold text-blue-900 bg-blue-50 group relative">
                            <div className="truncate" title={`${p.name} - ${p.dept}`}>
                              {p.name.split(' ').slice(0,1).join(' ')} {p.name.split(' ').slice(-1)}
                            </div>
                            <div className="text-[9px] text-gray-500 font-normal truncate opacity-70">
                              {p.dept}
                            </div>
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {schedule.map((row, idx) => (
                        <tr key={row.id} className="hover:bg-blue-50 transition-colors group">
                          <td className="p-1 border border-gray-200 text-center relative">
                            <span className="text-gray-400 text-xs">{idx + 1}</span>
                            <button 
                              onClick={() => removeRow(row.id)}
                              className="absolute left-0 top-0 h-full w-full bg-red-100 text-red-600 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity"
                              title="Satırı Sil"
                            >
                              <Icons.Trash2 size={14} />
                            </button>
                          </td>
                          <td className="p-1 border border-gray-200">
                            <input 
                              type="text" 
                              value={row.date}
                              onChange={(e) => handleRowInfoChange(row.id, 'date', e.target.value)}
                              placeholder="GG.AA.YYYY"
                              className="w-full px-2 py-1 text-xs border border-transparent focus:border-blue-500 rounded outline-none bg-transparent"
                            />
                          </td>
                          <td className="p-1 border border-gray-200">
                            <input 
                              type="text" 
                              value={row.desc}
                              onChange={(e) => handleRowInfoChange(row.id, 'desc', e.target.value)}
                              placeholder="Görev adı..."
                              className="w-full px-2 py-1 text-xs border border-transparent focus:border-blue-500 rounded outline-none bg-transparent"
                            />
                          </td>
                          {departmentSortedPersonnel.map(p => (
                            <td key={p.id} className="p-1 border border-gray-200 text-center">
                              <input 
                                type="text" 
                                value={row.assignments[p.id] || ''}
                                onChange={(e) => handleAssignmentChange(row.id, p.id, e.target.value)}
                                className="w-full text-center px-1 py-1 text-xs uppercase font-medium focus:bg-yellow-50 focus:ring-2 ring-blue-400 rounded outline-none transition-all placeholder-gray-200"
                                placeholder="-"
                              />
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {activeTab === 'list' && (
              <div className="flex flex-col h-full bg-white rounded-lg shadow border border-gray-200">
                <div className="p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
                  <div className="flex items-center gap-3">
                    <h2 className="font-bold text-gray-700">Personel Yönetimi</h2>
                    <button 
                      onClick={() => setShowAddPersonModal(true)} 
                      className="px-3 py-1.5 bg-blue-600 text-white rounded hover:bg-blue-700 flex items-center gap-1 text-xs shadow-sm"
                    >
                      <Icons.UserPlus size={14} /> Yeni Personel Ekle
                    </button>
                  </div>
                  <div className="flex items-center gap-2">
                     <div className="text-xs text-gray-500 mr-2 italic flex items-center gap-1">
                       <Icons.Info size={12}/> "TOPLAM" başlığına tıklayarak sıralama yapabilirsiniz.
                     </div>
                     <button onClick={() => exportToCSV('list')} className="px-3 py-1.5 bg-gray-600 text-white rounded hover:bg-gray-700 flex items-center gap-1 text-xs">
                      <Icons.Download size={14} /> Listeyi İndir (Excel)
                    </button>
                  </div>
                </div>
                <div className="flex-1 overflow-auto">
                  <table className="w-full border-collapse">
                    <thead className="bg-gray-800 text-white sticky top-0 shadow z-10">
                      <tr>
                        <th className="p-3 text-left w-12 text-xs">İşlem</th>
                        <th className="p-3 text-left w-12 text-xs">Sıra</th>
                        <th className="p-3 text-left w-48 text-xs">Adı Soyadı</th>
                        <th className="p-3 text-left w-48 text-xs hidden md:table-cell">Bölüm</th>
                        {settings.map(s => (
                          <th key={s.code} className="p-3 text-center text-xs w-20">
                            <div className="flex flex-col items-center">
                              <span>{s.label}</span>
                              <span className="text-[10px] opacity-70">({s.points} P)</span>
                            </div>
                          </th>
                        ))}
                        <th className="p-3 text-center w-24 text-xs bg-gray-700">Devir</th>
                        <th 
                          onClick={() => requestSort('totalScore')}
                          className="p-3 text-center w-24 text-xs font-bold bg-blue-900 cursor-pointer hover:bg-blue-700 transition-colors select-none group"
                        >
                          <div className="flex items-center justify-center gap-1">
                            TOPLAM
                            {sortConfig.key === 'totalScore' ? (
                              sortConfig.direction === 'desc' ? <Icons.ArrowDown size={14} className="text-yellow-400"/> : <Icons.ArrowUp size={14} className="text-yellow-400"/>
                            ) : (
                              <Icons.ArrowUpDown size={14} className="opacity-30 group-hover:opacity-100"/>
                            )}
                          </div>
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {sortedPersonnelList.map((p, idx) => {
                        const stats = calculatedStats[p.id];
                        const totalPoints = (stats.totalScore || 0) + (p.devir || 0);
                        return (
                          <tr key={p.id} className="hover:bg-gray-50 group">
                            <td className="p-3 text-center">
                              <button 
                                onClick={() => handleRemovePerson(p.id)}
                                className="text-gray-300 hover:text-red-600 transition-colors p-1"
                                title="Personeli Sil"
                              >
                                <Icons.Trash2 size={16} />
                              </button>
                            </td>
                            <td className="p-3 text-gray-500 text-center font-mono">{idx + 1}</td>
                            <td className="p-3 font-medium text-gray-800">{p.name}</td>
                            <td className="p-3 text-gray-500 text-xs hidden md:table-cell">{p.dept}</td>
                            {settings.map(s => (
                              <td key={s.code} className={`p-3 text-center font-mono ${stats.counts[s.code] > 0 ? 'text-blue-600 font-bold bg-blue-50/50' : 'text-gray-300'}`}>
                                {stats.counts[s.code] || '-'}
                              </td>
                            ))}
                            <td className="p-3 text-center text-gray-600 font-mono bg-gray-50">{p.devir}</td>
                            <td className="p-3 text-center font-bold text-white bg-blue-600 text-lg shadow-inner">
                              {totalPoints}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {activeTab === 'settings' && (
              <div className="p-8 max-w-4xl mx-auto w-full">
                <div className="bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden">
                  <div className="p-6 border-b border-gray-100 bg-gray-50">
                    <h2 className="text-lg font-bold text-gray-800 flex items-center gap-2">
                      <Icons.Settings className="text-gray-500" />
                      Görev ve Puan Ayarları
                    </h2>
                  </div>
                  <div className="p-6 space-y-8">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {settings.map(s => (
                        <div key={s.code} className="flex items-center p-4 bg-white border border-gray-200 rounded-lg shadow-sm">
                          <div className="w-12 h-12 flex items-center justify-center bg-blue-100 text-blue-700 font-bold text-xl rounded-full mr-4">
                            {s.code}
                          </div>
                          <div>
                            <h3 className="font-bold text-gray-800">{s.label}</h3>
                            <p className="text-green-600 font-medium">{s.points} Puan</p>
                          </div>
                        </div>
                      ))}
                    </div>
                    
                    <div className="p-4 bg-gray-50 border border-gray-200 rounded-md">
                       <h4 className="font-bold text-gray-700 mb-2 flex items-center gap-2"><Icons.Save size={16}/> Veri Kaydı Hakkında</h4>
                       <p className="text-sm text-gray-600 mb-4">
                         Tüm verileriniz (yeni eklenen personeller, görev girişleri vb.) tarayıcınıza otomatik kaydedilir. 
                         Sayfayı kapatsanız bile geri geldiğinizde verileriniz burada durur.
                       </p>
                       <button 
                        onClick={resetData}
                        className="px-4 py-2 bg-red-100 text-red-700 border border-red-200 rounded hover:bg-red-200 flex items-center gap-2 text-sm font-medium"
                       >
                         <Icons.RefreshCw size={14}/> Tüm Verileri Sıfırla (Fabrika Ayarları)
                       </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
          </main>
        </div>
      );
    }

    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
  </script>
</body>
</html>
"""

# HTML/JS kodunu Streamlit içinde tam ekran çalıştır
components.html(html_code, height=1000, scrolling=True)
