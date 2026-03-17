import React, { useState } from 'react';

const FmsButton = ({ children, variant = 'primary', disabled = false, onClick, className = '' }) => {
  const baseStyles = "px-6 py-2 rounded-md font-bold transition-all duration-200 active:scale-95 text-sm";
  const variants = {
    primary: "bg-[#126eb4] text-white hover:bg-[#423c3b] disabled:bg-[#d3d3d3] disabled:text-gray-500",
    secondary: "bg-white text-[#126eb4] border border-[#126eb4] hover:bg-gray-50 disabled:border-gray-200 disabled:text-gray-400",
    danger: "bg-[#c63c2c] text-white hover:bg-[#423c3b] disabled:bg-[#d3d3d3]",
  };
  return (
    <button onClick={onClick} disabled={disabled} className={`${baseStyles} ${variants[variant]} ${className}`}>
      {children}
    </button>
  );
};

const FmsStandardDemo = () => {
  const [vehicles] = useState([
    { id: 1, license: 'ABC-1234', driver: '林小明', status: '行駛中' },
    { id: 2, license: 'EUP-8888', driver: '陳大華', status: '待命中' },
  ]);

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-20">
      {/* 1. 按鈕狀態規範區 */}
      <section className="space-y-4">
        <h3 className="text-sm font-bold text-gray-400 uppercase tracking-widest ml-1">按鈕狀態規範 (Button States)</h3>
        <div className="bg-white p-6 rounded-3xl shadow-xl shadow-blue-900/5 space-y-6 border border-gray-50">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <p className="text-[10px] text-gray-400 font-bold">PRIMARY (DEFAULT)</p>
              <FmsButton variant="primary" className="w-full">主要按鈕</FmsButton>
            </div>
            <div className="space-y-2">
              <p className="text-[10px] text-gray-400 font-bold">PRIMARY (DISABLED)</p>
              <FmsButton variant="primary" disabled className="w-full">禁用按鈕</FmsButton>
            </div>
            <div className="space-y-2">
              <p className="text-[10px] text-gray-400 font-bold">DANGER / ALT</p>
              <FmsButton variant="danger" className="w-full">刪除類按鈕</FmsButton>
            </div>
            <div className="space-y-2">
              <p className="text-[10px] text-gray-400 font-bold">SECONDARY</p>
              <FmsButton variant="secondary" className="w-full">次要按鈕</FmsButton>
            </div>
          </div>
          <div className="bg-blue-50 p-3 rounded-xl text-[11px] text-blue-600 font-medium leading-relaxed">
            💡 觀測點：請將滑鼠移至「主要按鈕」，背景色會從品牌藍轉為規範要求的 **炭灰色 (#423c3b)**。
          </div>
        </div>
      </section>

      {/* 2. 列表互動規範區 */}
      <section className="space-y-4">
        <h3 className="text-sm font-bold text-gray-400 uppercase tracking-widest ml-1">列表互動展示 (Hover Actions)</h3>
        <div className="bg-white rounded-3xl shadow-xl shadow-blue-900/5 overflow-hidden border border-gray-50">
          {vehicles.map((car) => (
            <div 
              key={car.id} 
              className="group relative flex items-center justify-between p-5 border-b last:border-0 hover:bg-blue-50/50 transition cursor-default select-none"
              onContextMenu={(e) => {
                e.preventDefault();
                alert('❌ 規範提醒：此區域已禁用右鍵選單功能');
              }}
              onDoubleClick={() => alert('📖 規範提醒：雙擊開啟詳情 (非編輯模式)')}
            >
              <div>
                <p className="font-mono font-bold text-[#126eb4] text-lg">{car.license}</p>
                <p className="text-sm text-gray-400 font-medium">{car.driver} · {car.status}</p>
              </div>

              {/* Hover Actions */}
              <div className="opacity-0 group-hover:opacity-100 flex items-center space-x-3 transition-all duration-200">
                <button className="text-[#126eb4] font-bold text-sm bg-white px-3 py-1.5 rounded-md border border-gray-100 shadow-sm hover:bg-gray-50">
                  編輯
                </button>
                <button className="text-[#c63c2c] font-bold text-sm bg-red-50/50 px-3 py-1.5 rounded-md border border-red-50 hover:bg-red-100">
                  刪除
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showDemo, setShowDemo] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'https://jennycargo-system.onrender.com';
      const response = await fetch(`${apiUrl}/api/track?q=${query}`);
      if (!response.ok) throw new Error('查無資料');
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-4">
      <header className="w-full max-w-md py-8 text-center flex flex-col items-center">
        <div className="bg-[#126eb4] text-white text-[10px] font-bold px-2 py-0.5 rounded-full mb-2 uppercase tracking-widest">Official</div>
        <h1 className="text-4xl font-bold text-[#126eb4] tracking-tight">JennyCargo</h1>
        <div className="flex mt-4 space-x-4">
          <button 
            onClick={() => {setShowDemo(false); setResult(null);}} 
            className={`text-sm font-bold pb-1 transition-all ${!showDemo ? 'text-[#126eb4] border-b-2 border-[#126eb4]' : 'text-gray-400'}`}
          >
            貨態查詢
          </button>
          <button 
            onClick={() => setShowDemo(true)} 
            className={`text-sm font-bold pb-1 transition-all ${showDemo ? 'text-[#126eb4] border-b-2 border-[#126eb4]' : 'text-gray-400'}`}
          >
            FMS 規範 Demo
          </button>
        </div>
      </header>

      <main className="w-full max-w-md space-y-6 pb-20">
        {!showDemo ? (
          <>
            <div className="bg-white rounded-3xl shadow-xl shadow-blue-900/5 p-6 space-y-4 border border-white">
              <div className="space-y-2">
                <label className="text-xs font-bold text-gray-300 uppercase tracking-wider ml-1">即時追蹤</label>
                <input
                  type="text"
                  className="w-full px-5 py-4 rounded-2xl bg-gray-50 border-2 border-transparent focus:bg-white focus:border-[#126eb4] outline-none transition-all text-lg"
                  placeholder="輸入號碼"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                />
              </div>
              <button
                onClick={handleSearch}
                disabled={loading}
                className="w-full bg-[#126eb4] hover:bg-[#007bc3] text-white font-bold py-4 rounded-2xl transition-all shadow-lg shadow-blue-100 active:scale-[0.98] disabled:opacity-50"
              >
                {loading ? '請稍候...' : '開始查詢'}
              </button>
            </div>

            {error && <div className="bg-red-50 text-red-600 p-4 rounded-2xl text-center font-medium">⚠️ {error}</div>}

            {result && (
              <div className="bg-white rounded-3xl shadow-xl shadow-blue-900/5 overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-500 border border-white">
                <div className="bg-[#126eb4] p-6 text-white text-center">
                  <p className="text-blue-100 text-xs font-bold uppercase tracking-widest mb-1">當前狀態</p>
                  <h2 className="text-3xl font-bold">{result.status}</h2>
                </div>
                <div className="p-6 space-y-4">
                  <div className="flex justify-between text-sm"><span className="text-gray-400">目前位置</span><span className="font-bold text-gray-700">{result.location}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-gray-400">預計抵達</span><span className="font-bold text-gray-700">{result.eta}</span></div>
                </div>
              </div>
            )}
          </>
        ) : (
          <FmsStandardDemo />
        )}
      </main>

      <footer className="fixed bottom-6 text-center text-[10px] text-gray-300 uppercase tracking-[0.2em] pointer-events-none">
        FMS Standardized UI · v2026.3
      </footer>
    </div>
  );
}

export default App;
