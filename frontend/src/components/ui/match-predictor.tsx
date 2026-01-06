"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Loader2, Trophy } from "lucide-react";
import { cn } from "../../lib/utils";

const TEAMS = [
  "Algeria", "Argentina", "Australia", "Austria", "Belgium", "Brazil", 
  "Canada", "Cape Verde", "Colombia", "Croatia", "Curaçao", "Ecuador", 
  "Egypt", "England", "France", "Germany", "Ghana", "Haiti", 
  "Iran", "Ivory Coast", "Japan", "Jordan", "Mexico", "Netherlands", 
  "New Zealand", "Panama", "Portugal", "Qatar", "Saudi Arabia", "Scotland", 
  "South Africa", "South Korea", "Spain", "Switzerland", "Tunisia", 
  "United States", "Uruguay", "Uzbekistan"
].sort();

export function MatchPredictor() {
  const [homeTeam, setHomeTeam] = useState("");
  const [awayTeam, setAwayTeam] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handlePredict = async () => {
    if (!homeTeam || !awayTeam) return;
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          home_team: homeTeam,
          away_team: awayTeam,
          neutral_venue: true
        }),
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto mt-8 p-6 bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl">
      <div className="flex flex-col gap-4">
        {/* Selectors */}
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="text-xs text-white/50 uppercase tracking-wider">Home Team</label>
            <select 
              className="w-full bg-black/50 border border-white/10 rounded-lg p-2 text-white outline-none focus:border-indigo-500 transition-colors"
              value={homeTeam}
              onChange={(e) => setHomeTeam(e.target.value)}
            >
              <option value="">Select...</option>
              {TEAMS.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>

          <div className="space-y-2">
            <label className="text-xs text-white/50 uppercase tracking-wider">Away Team</label>
            <select 
              className="w-full bg-black/50 border border-white/10 rounded-lg p-2 text-white outline-none focus:border-rose-500 transition-colors"
              value={awayTeam}
              onChange={(e) => setAwayTeam(e.target.value)}
            >
              <option value="">Select...</option>
              {TEAMS.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
        </div>

        {/* Action Button */}
        <button
          onClick={handlePredict}
          disabled={loading || !homeTeam || !awayTeam}
          className={cn(
            "w-full py-3 rounded-lg font-medium transition-all duration-300",
            "bg-gradient-to-r from-indigo-500 to-rose-500 hover:opacity-90",
            "disabled:opacity-50 disabled:cursor-not-allowed"
          )}
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin" /> Analyzing...
            </span>
          ) : (
            "Predict Winner"
          )}
        </button>

        {/* Results Card */}
        {result && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 p-4 rounded-lg bg-white/10 border border-white/20 text-center"
          >
            <div className="flex items-center justify-center gap-2 mb-2">
              <Trophy className="h-5 w-5 text-yellow-400" />
              <span className="text-sm text-white/70">Predicted Outcome</span>
            </div>
            <h3 className="text-2xl font-bold text-white mb-1">
              {result.prediction}
            </h3>
            
            {/* Probability Bars */}
            <div className="grid grid-cols-3 gap-2 mt-4 text-xs text-white/50">
              <div className="flex flex-col gap-1">
                <span>Home</span>
                <div className="h-1 bg-white/20 rounded-full overflow-hidden">
                  <div className="h-full bg-indigo-500" style={{ width: `${result.probability.home_win * 100}%` }} />
                </div>
                <span>{(result.probability.home_win * 100).toFixed(0)}%</span>
              </div>
              <div className="flex flex-col gap-1">
                <span>Draw</span>
                <div className="h-1 bg-white/20 rounded-full overflow-hidden">
                  <div className="h-full bg-gray-500" style={{ width: `${result.probability.draw * 100}%` }} />
                </div>
                <span>{(result.probability.draw * 100).toFixed(0)}%</span>
              </div>
              <div className="flex flex-col gap-1">
                <span>Away</span>
                <div className="h-1 bg-white/20 rounded-full overflow-hidden">
                  <div className="h-full bg-rose-500" style={{ width: `${result.probability.away_win * 100}%` }} />
                </div>
                <span>{(result.probability.away_win * 100).toFixed(0)}%</span>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
