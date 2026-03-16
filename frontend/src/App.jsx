import React, { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    setError('');
    setResult(null);

    try {
      // 使用環境變數或預設的 Render 網址
      const apiUrl = import.meta.env.VITE_API_URL || 'https://jennycargo-system.onrender.com';
      const response = await fetch(`${apiUrl}/api/track?q=${query}`);
      if (!response.ok) {
        throw new Error('查無資料，請確認輸入是否正確。');
      }
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
      {/* Header */}
      <header className="w-full max-w-md py-8 text-center">
        <h1 className="text-4xl font-bold text-[#126eb4] tracking-tight">JennyCargo</h1>
        <p className="text-gray-500 mt-2">智能貨態追蹤系統</p>
      </header>

      {/* Search Section */}
      <main className="w-full max-w-md space-y-6">
        <div className="bg-white rounded-3xl shadow-xl shadow-blue-900/5 p-6 space-y-4">
          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-400 uppercase tracking-wider ml-1">查詢資訊</label>
            <input
              type="text"
              className="w-full px-5 py-4 rounded-2xl border-2 border-gray-50 focus:border-[#126eb4] focus:ring-4 focus:ring-blue-100 outline-none transition-all text-lg"
              placeholder="客戶編號 / 統編 / 單號"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            />
          </div>
          <button
            onClick={handleSearch}
            disabled={loading}
            className="w-full bg-[#126eb4] hover:bg-[#007bc3] text-white font-bold py-4 rounded-2xl transition-all shadow-lg shadow-blue-200 active:scale-[0.98] disabled:opacity-50"
          >
            {loading ? '查詢中...' : '立即追蹤'}
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 text-red-600 p-4 rounded-2xl text-center font-medium animate-pulse">
            ⚠️ {error}
          </div>
        )}

        {/* Result Display */}
        {result && (
          <div className="bg-white rounded-3xl shadow-xl shadow-blue-900/5 overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="bg-[#126eb4] p-6 text-white">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-blue-100 text-xs font-bold uppercase tracking-widest">當前狀態</p>
                  <h2 className="text-3xl font-bold mt-1">{result.status}</h2>
                </div>
                <div className="text-right">
                  <p className="text-blue-100 text-xs font-bold uppercase tracking-widest">單號</p>
                  <p className="font-mono text-sm">{result.tid}</p>
                </div>
              </div>
            </div>
            
            <div className="p-6 space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-gray-50 rounded-2xl">
                  <p className="text-gray-400 text-[10px] font-bold uppercase">最後位置</p>
                  <p className="font-bold text-gray-700">{result.location}</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-2xl">
                  <p className="text-gray-400 text-[10px] font-bold uppercase">預計抵達</p>
                  <p className="font-bold text-gray-700">{result.eta}</p>
                </div>
              </div>

              {/* Timeline */}
              <div className="space-y-4">
                <p className="text-gray-400 text-[10px] font-bold uppercase tracking-wider">物流軌跡</p>
                <div className="space-y-4 relative before:absolute before:inset-0 before:left-2 before:w-0.5 before:bg-gray-100">
                  {result.history.map((step, idx) => (
                    <div key={idx} className="relative pl-8">
                      <div className={`absolute left-0 top-1.5 w-4 h-4 rounded-full border-4 border-white shadow-sm ${idx === 0 ? 'bg-[#126eb4] scale-125' : 'bg-gray-300'}`}></div>
                      <p className={`text-sm ${idx === 0 ? 'text-gray-800 font-bold' : 'text-gray-500'}`}>{step}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-auto py-8 text-center text-xs text-gray-400">
        Powered by Jenny_First AI System
      </footer>
    </div>
  );
}

export default App;
