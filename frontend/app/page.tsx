import { HeroGeometric } from "../src/components/ui/shape-landing-hero";
import { MatchPredictor } from "../src/components/ui/match-predictor";

export default function Home() {
  return (
    <main className="min-h-screen bg-black">
      <HeroGeometric 
        // We removed the badge prop so it won't show
        title1="FIFA World Cup"
        title2="Prediction" 
      >
        <MatchPredictor />
      </HeroGeometric>
    </main>
  );
}
