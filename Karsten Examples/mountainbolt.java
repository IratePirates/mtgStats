 //Original article found at:
 //http://www.channelfireball.com/articles/frank-analysis-optimal-decks-for-ten-new-goldfish-formats/
 
 public class MountainBolt {

    public static void main(String[] args) {
        
        Deck deck=new Deck();
        boolean[][][][][][] KeepOpeningHand = new boolean[8][8][8][8][8][8];
        boolean TakeTimeToFindOptimalMulliganStrategy = false;
        if (TakeTimeToFindOptimalMulliganStrategy==false) {KeepOpeningHand=GiveLooseMulliganStrategy();}
        int NumberOfSimulationsPerDeck=2000;
        double FastestTurn=50;
        double KillTurn;
        int OptimalOneDrops=0;
        int OptimalTwoDrops=0;
        int OptimalThreeDrops=0;
        int OptimalBolts=0;
        int OptimalLands=0;

        
        for (int BoltCount=10; BoltCount<=55; BoltCount++){
            deck.SetDeck(0,0,0,BoltCount,60-BoltCount);
            deck.PrintDeckBrief();
            if (TakeTimeToFindOptimalMulliganStrategy==true) {KeepOpeningHand=GiveOptimalMulliganStrategy(deck);}
            KillTurn=AverageKillTurnForRandomHand(deck,7,KeepOpeningHand,NumberOfSimulationsPerDeck);
            System.out.println(" "+KillTurn);
            if (KillTurn<FastestTurn){
                FastestTurn=KillTurn;
                OptimalBolts=BoltCount; 
            }
        }
        
        System.out.println("----------------");
        System.out.print("The optimal deck after the grid-enumeration at a small number of simulations per deck was:");
        deck.SetDeck(OptimalOneDrops,OptimalTwoDrops,OptimalThreeDrops,OptimalBolts,60-OptimalBolts);
        deck.PrintDeckBrief();
        System.out.println();
        System.out.println("----------------");
        
        TakeTimeToFindOptimalMulliganStrategy=true;
        NumberOfSimulationsPerDeck=500000;
        FastestTurn=50;
        boolean ContinueLocalSearch=true;
        
        for (int BoltCount=Math.max(0,OptimalBolts-4); BoltCount<=Math.min(60,OptimalBolts+4); BoltCount++){
            deck.SetDeck(0,0,0,BoltCount,60-BoltCount);
            deck.PrintDeckBrief();
            System.out.println();
            if (TakeTimeToFindOptimalMulliganStrategy==true) {KeepOpeningHand=GiveOptimalMulliganStrategy(deck);}
            KillTurn=AverageKillTurnForRandomHand(deck,7,KeepOpeningHand,NumberOfSimulationsPerDeck);
            deck.PrintDeckBrief(); System.out.println(" "+KillTurn);
            if (KillTurn<FastestTurn){
                FastestTurn=KillTurn;
                OptimalBolts=BoltCount; 
            }
        }
        
        System.out.println("----------------");
        System.out.print("The final optimal deck:");
        deck.SetDeck(0,0,0,OptimalBolts,60-OptimalBolts);
        deck.PrintDeckBrief();
        System.out.println();
        System.out.println("----------------");
    }//end of main
  
    public static boolean[][][][][][] GiveOptimalMulliganStrategy(Deck deck) {
        boolean[][][][][][] KeepOpeningHand = new boolean[8][8][8][8][8][8];
        OpeningHand openinghand=new OpeningHand();
        int NumberOfSimulationsPerOpeningHandSize=10000;
        int OriginalNr1Cost=deck.NumberOf1Cost;
        int OriginalNr2Cost=deck.NumberOf2Cost;
        int OriginalNr3Cost=deck.NumberOf3Cost;
        int OriginalNrBolts=deck.NumberOfBolts;
        int OriginalNrLands=deck.NumberOfLands;
        double CutOffTurn = AverageKillTurnForRandomHand(deck,1,KeepOpeningHand,NumberOfSimulationsPerOpeningHandSize);
        for (int StartingCards=2; StartingCards<=7; StartingCards++){
            System.out.print(".");
            for (int OneDropCount=0; OneDropCount<=OriginalNr1Cost && OneDropCount<=StartingCards; OneDropCount++){
                for (int TwoDropCount=0; TwoDropCount<=OriginalNr2Cost && TwoDropCount+OneDropCount<=StartingCards; TwoDropCount++){
                    for  (int ThreeDropCount=0; ThreeDropCount<=OriginalNr3Cost && ThreeDropCount+TwoDropCount+OneDropCount<=StartingCards; ThreeDropCount++){
                        for (int BoltCount=0; BoltCount<=OriginalNrBolts && BoltCount+ThreeDropCount+TwoDropCount+OneDropCount<=StartingCards; BoltCount++){
                            int LandCount=StartingCards-OneDropCount-TwoDropCount-ThreeDropCount-BoltCount;
                            if (LandCount<=OriginalNrLands){
                                openinghand.SetHand(OneDropCount, TwoDropCount, ThreeDropCount, BoltCount, LandCount);
                                deck.SetDeck(OriginalNr1Cost,OriginalNr2Cost,OriginalNr3Cost,OriginalNrBolts,OriginalNrLands);
                                double AvgKillTurn=AverageKillTurnForSpecificHand(deck,openinghand);
                                if (AvgKillTurn<=CutOffTurn) { KeepOpeningHand[StartingCards][OneDropCount][TwoDropCount][ThreeDropCount][BoltCount][LandCount]=true; System.out.println(BoltCount+ " Bolts in "+StartingCards+" cards is keep");}
                                if (AvgKillTurn>CutOffTurn) { KeepOpeningHand[StartingCards][OneDropCount][TwoDropCount][ThreeDropCount][BoltCount][LandCount]=false; System.out.println(BoltCount+ " Bolts in "+StartingCards+" cards is mull");}
                                }
                            }
                        }
                    }
                }
            deck.SetDeck(OriginalNr1Cost,OriginalNr2Cost,OriginalNr3Cost,OriginalNrBolts,OriginalNrLands);
            if (StartingCards<7) {CutOffTurn=AverageKillTurnForRandomHand(deck,StartingCards,KeepOpeningHand,NumberOfSimulationsPerOpeningHandSize);}
        }
        return KeepOpeningHand;
    }
 
    public static boolean[][][][][][] GiveLooseMulliganStrategy() {
        boolean[][][][][][] KeepOpeningHand = new boolean[8][8][8][8][8][8];
        for (int StartingCards=2; StartingCards<=7; StartingCards++){
            for (int OneDropCount=0; OneDropCount<=StartingCards; OneDropCount++){
                for (int TwoDropCount=0; TwoDropCount+OneDropCount<=StartingCards; TwoDropCount++){
                    for  (int ThreeDropCount=0; ThreeDropCount+TwoDropCount+OneDropCount<=StartingCards; ThreeDropCount++){
                        for (int BoltCount=0; BoltCount+ThreeDropCount+TwoDropCount+OneDropCount<=StartingCards; BoltCount++){
                            int LandCount=StartingCards-OneDropCount-TwoDropCount-ThreeDropCount-BoltCount;
                            KeepOpeningHand[StartingCards][OneDropCount][TwoDropCount][ThreeDropCount][BoltCount][LandCount]=false;
                            if (LandCount>=1 && LandCount<=3) {KeepOpeningHand[StartingCards][OneDropCount][TwoDropCount][ThreeDropCount][BoltCount][LandCount]=true;}
                        }
                    }
                }
            }
        }
        return KeepOpeningHand;
    }
   
    public static double AverageKillTurnForSpecificHand(Deck deck, OpeningHand openinghand){
        int NumberOfIterations=2000;
        Deck remainingdeck=new Deck();
        double AverageKillTurn=0;
        for (int IterationCounter=1; IterationCounter<=NumberOfIterations; IterationCounter++){
            remainingdeck.SetDeck(deck.NumberOf1Cost-openinghand.NumberOf1Cost,deck.NumberOf2Cost-openinghand.NumberOf2Cost,deck.NumberOf3Cost-openinghand.NumberOf3Cost,deck.NumberOfBolts-openinghand.NumberOfBolts,deck.NumberOfLands-openinghand.NumberOfLands);
            AverageKillTurn=AverageKillTurn+TurnKill(remainingdeck,openinghand);
        }
        return (AverageKillTurn/(NumberOfIterations+0.0));
    }//end of AverageKillTurnForSpecificHand
 
    public static double AverageKillTurnForRandomHand(Deck deck, int StartingCards, boolean[][][][][][] KeepOpeningHand, int NumberOfIterations){
        Deck remainingdeck=new Deck();
        double AverageKillTurn=0;
        for (int IterationCounter=1; IterationCounter<=NumberOfIterations; IterationCounter++){
            OpeningHand openinghand=GiveOpeningHandAfterMulls(deck, StartingCards, KeepOpeningHand);
            remainingdeck.SetDeck(deck.NumberOf1Cost-openinghand.NumberOf1Cost,deck.NumberOf2Cost-openinghand.NumberOf2Cost,deck.NumberOf3Cost-openinghand.NumberOf3Cost,deck.NumberOfBolts-openinghand.NumberOfBolts,deck.NumberOfLands-openinghand.NumberOfLands);
            AverageKillTurn=AverageKillTurn+TurnKill(remainingdeck,openinghand);
            if ( IterationCounter % 200000 == 0) {System.out.print(".");}
        }
        return AverageKillTurn/(NumberOfIterations+0.0);
    }//end of AverageKillTurnForRandomHand
   
    static OpeningHand GiveOpeningHandAfterMulls (Deck deck, int StartingCards, boolean[][][][][][] KeepOpeningHand) {
       
        Deck remainingdeck=new Deck();
        OpeningHand openinghand=new OpeningHand();
        int TypeOfCardDrawn;
        boolean KeepHand=false;
       
        for (int OpeningHandSize=7; OpeningHandSize>=1; OpeningHandSize--){
            if (KeepHand==false && StartingCards>=OpeningHandSize){
                openinghand.ResetHand();
                remainingdeck.SetDeck(deck.NumberOf1Cost,deck.NumberOf2Cost,deck.NumberOf3Cost,deck.NumberOfBolts,deck.NumberOfLands);
                for (int CardsDrawn=0; CardsDrawn<OpeningHandSize; CardsDrawn++){
                    TypeOfCardDrawn=remainingdeck.DrawCard();
                    if (TypeOfCardDrawn==1) {openinghand.NumberOf1Cost++;}
                    if (TypeOfCardDrawn==2) {openinghand.NumberOf2Cost++;}
                    if (TypeOfCardDrawn==3) {openinghand.NumberOf3Cost++;}
                    if (TypeOfCardDrawn==4) {openinghand.NumberOfBolts++;}
                    if (TypeOfCardDrawn==5) {openinghand.NumberOfLands++;}
                }
                KeepHand=true;
                if (OpeningHandSize>1) {
                    if (KeepOpeningHand[OpeningHandSize][openinghand.NumberOf1Cost][openinghand.NumberOf2Cost][openinghand.NumberOf3Cost][openinghand.NumberOfBolts][openinghand.NumberOfLands]==false) {KeepHand=false;}
                }
            }
        }
       
        return openinghand;
    }//end of GiveOpeningHandAfterMulls
    
    static int TurnKill(Deck remainingdeck, OpeningHand openinghand) {
       
        int OneCostPower=1;
        int TwoCostPower=2;
        int ThreeCostPower=3;
        int BoltDamage=3;
       
        int Turn=0;
        int OppLife=20;
        int ManaLeft;
        int TypeOfCardDrawn;
   
        int OneDropsInPlay=0;
        int TwoDropsInPlay=0;
        int ThreeDropsInPlay=0;
        int LandsInPlay=0;
       
        int OneDropsInHand=openinghand.NumberOf1Cost;
        int TwoDropsInHand=openinghand.NumberOf2Cost;
        int ThreeDropsInHand=openinghand.NumberOf3Cost;
        int BoltsInHand=openinghand.NumberOfBolts;
        int LandsInHand=openinghand.NumberOfLands;
       
        do {
           
            Turn++;
           
            if (Turn==1) {
               
                if (LandsInHand>=1) {LandsInPlay++; LandsInHand--;}
                ManaLeft=LandsInPlay;
                if (OneDropsInHand>=1 && ManaLeft==1) {OneDropsInPlay++; ManaLeft--; OneDropsInHand--;}
                if (BoltsInHand>=1 && ManaLeft==1) {OppLife=OppLife-BoltDamage; ManaLeft--; BoltsInHand--;}
               
            } //end of the first turn
           
            if (Turn>1) {
 
                TypeOfCardDrawn=remainingdeck.DrawCard();
                if (TypeOfCardDrawn==1) {OneDropsInHand++;}
                if (TypeOfCardDrawn==2) {TwoDropsInHand++;}
                if (TypeOfCardDrawn==3) {ThreeDropsInHand++;}
                if (TypeOfCardDrawn==4) {BoltsInHand++;}
                if (TypeOfCardDrawn==5) {LandsInHand++;}
 
                if (LandsInHand>=1) {LandsInPlay++; LandsInHand--;}
                ManaLeft=LandsInPlay;
                OppLife=OppLife-OneCostPower*OneDropsInPlay;
                OppLife=OppLife-TwoCostPower*TwoDropsInPlay;
                OppLife=OppLife-ThreeCostPower*ThreeDropsInPlay;
               
                if (ManaLeft==1) {
                    int CastableBolts=Math.min(BoltsInHand, ManaLeft);
                    if (OppLife<=CastableBolts*BoltDamage) {OppLife=OppLife-CastableBolts*BoltDamage; ManaLeft=ManaLeft-CastableBolts; BoltsInHand=BoltsInHand-CastableBolts;}
                    if (OneDropsInHand>=1 && ManaLeft==1) {OneDropsInPlay++; ManaLeft--; OneDropsInHand--;}
                    if (BoltsInHand>=1 && ManaLeft==1) {OppLife=OppLife-BoltDamage; ManaLeft--; BoltsInHand--;}
                }
               
                if (ManaLeft==2) {
                    int CastableBolts=Math.min(BoltsInHand, ManaLeft);
                    if (OppLife<=CastableBolts*BoltDamage) {OppLife=OppLife-CastableBolts*BoltDamage; ManaLeft=ManaLeft-CastableBolts; BoltsInHand=BoltsInHand-CastableBolts;}
                    if (TwoDropsInHand>=1 && ManaLeft==2) {TwoDropsInPlay++; ManaLeft=ManaLeft-2; TwoDropsInHand--;}
                    int CastableOneDrops=Math.min(OneDropsInHand, ManaLeft);
                    if (CastableOneDrops>=1) {OneDropsInPlay=OneDropsInPlay+CastableOneDrops; ManaLeft=ManaLeft-CastableOneDrops; OneDropsInHand=OneDropsInHand-CastableOneDrops;}
                    CastableBolts=Math.min(BoltsInHand, ManaLeft);
                    if (CastableBolts>=1) {OppLife=OppLife-CastableBolts*BoltDamage; ManaLeft=ManaLeft-CastableBolts; BoltsInHand=BoltsInHand-CastableBolts;}
                }
 
                if (ManaLeft==3) {
                    int CastableBolts=Math.min(BoltsInHand, ManaLeft);
                    if (OppLife<=CastableBolts*BoltDamage) {OppLife=OppLife-CastableBolts*BoltDamage; ManaLeft=ManaLeft-CastableBolts; BoltsInHand=BoltsInHand-CastableBolts;}
                    if (ThreeDropsInHand>=1 && ManaLeft==3) {ThreeDropsInPlay++; ManaLeft=ManaLeft-3; ThreeDropsInHand--;}
                    if (TwoDropsInHand>=1 && ManaLeft>=2) {TwoDropsInPlay++; ManaLeft=ManaLeft-2; TwoDropsInHand--;}
                    int CastableOneDrops=Math.min(OneDropsInHand, ManaLeft);
                    if (CastableOneDrops>=1) {OneDropsInPlay=OneDropsInPlay+CastableOneDrops; ManaLeft=ManaLeft-CastableOneDrops; OneDropsInHand=OneDropsInHand-CastableOneDrops;}
                    CastableBolts=Math.min(BoltsInHand, ManaLeft);
                    if (CastableBolts>=1) {OppLife=OppLife-CastableBolts*BoltDamage; ManaLeft=ManaLeft-CastableBolts; BoltsInHand=BoltsInHand-CastableBolts;}
                }
               
                if (ManaLeft==4) {
                    int CastableBolts=Math.min(BoltsInHand, ManaLeft);
                    if (OppLife<=CastableBolts*BoltDamage) {OppLife=OppLife-CastableBolts*BoltDamage; ManaLeft=ManaLeft-CastableBolts; BoltsInHand=BoltsInHand-CastableBolts;}
                    int CastableTwoDrops=Math.min(TwoDropsInHand, ManaLeft/2);
                    if (CastableTwoDrops==2) {TwoDropsInPlay=TwoDropsInPlay+2; ManaLeft=ManaLeft-4; TwoDropsInHand=TwoDropsInHand-2;}
                    if (ThreeDropsInHand>=1 && ManaLeft>=3) {ThreeDropsInPlay++; ManaLeft=ManaLeft-3; ThreeDropsInHand--;}
                    if (TwoDropsInHand>=1 && ManaLeft>=2) {TwoDropsInPlay++; ManaLeft=ManaLeft-2; TwoDropsInHand--;}
                    int CastableOneDrops=Math.min(OneDropsInHand, ManaLeft);
                    if (CastableOneDrops>=1) {OneDropsInPlay=OneDropsInPlay+CastableOneDrops; ManaLeft=ManaLeft-CastableOneDrops; OneDropsInHand=OneDropsInHand-CastableOneDrops;}
                    CastableBolts=Math.min(BoltsInHand, ManaLeft);
                    if (CastableBolts>=1) {OppLife=OppLife-CastableBolts*BoltDamage; ManaLeft=ManaLeft-CastableBolts; BoltsInHand=BoltsInHand-CastableBolts;}
                }
                       
                if (ManaLeft>=5) {
                    int CastableBolts=Math.min(BoltsInHand, ManaLeft);
                    if (OppLife<=CastableBolts*BoltDamage) {OppLife=OppLife-CastableBolts*BoltDamage; ManaLeft=ManaLeft-CastableBolts; BoltsInHand=BoltsInHand-CastableBolts;}
                    int CastableThreeDrops=Math.min(ThreeDropsInHand, ManaLeft/3);
                    if (CastableThreeDrops>=1) {ThreeDropsInPlay=ThreeDropsInPlay+CastableThreeDrops; ManaLeft=ManaLeft-3*CastableThreeDrops; ThreeDropsInHand=ThreeDropsInHand-CastableThreeDrops;}
                    int CastableTwoDrops=Math.min(TwoDropsInHand, ManaLeft/2);
                    if (CastableTwoDrops>=1) {TwoDropsInPlay=TwoDropsInPlay+CastableTwoDrops; ManaLeft=ManaLeft-2*CastableTwoDrops; TwoDropsInHand=TwoDropsInHand-CastableTwoDrops;}
                    int CastableOneDrops=Math.min(OneDropsInHand, ManaLeft);
                    if (CastableOneDrops>=1) {OneDropsInPlay=OneDropsInPlay+CastableOneDrops; ManaLeft=ManaLeft-CastableOneDrops; OneDropsInHand=OneDropsInHand-CastableOneDrops;}
                    CastableBolts=Math.min(BoltsInHand, ManaLeft);
                    if (CastableBolts>=1) {OppLife=OppLife-CastableBolts*BoltDamage; ManaLeft=ManaLeft-CastableBolts; BoltsInHand=BoltsInHand-CastableBolts;}
                }
               
            } //end of a turn in which we drew a card and attacked
 
        } while (OppLife>0 &&Turn<=50);
       
        return Turn;
    }//end of TurnKill
    
    
}//end of OptimalAggroGoldfishDeck

class OpeningHand {
    int NumberOf1Cost;
    int NumberOf2Cost;
    int NumberOf3Cost;
    int NumberOfBolts;
    int NumberOfLands;
 
    void ResetHand(){
        NumberOf1Cost=0;
        NumberOf2Cost=0;
        NumberOf3Cost=0;
        NumberOfBolts=0;
        NumberOfLands=0;
    }
           
    void SetHand (int Nr1Cost, int Nr2Cost, int Nr3Cost, int NrBolts, int NrLands) {
        NumberOf1Cost=Nr1Cost;
        NumberOf2Cost=Nr2Cost;
        NumberOf3Cost=Nr3Cost;
        NumberOfBolts=NrBolts;
        NumberOfLands=NrLands;
    }
 
}//end of OpeningHand
 
class Deck {
    int NumberOf1Cost;
    int NumberOf2Cost;
    int NumberOf3Cost;
    int NumberOfBolts;
    int NumberOfLands;
 
    void PrintDeckBrief () {
        if(NumberOf1Cost<10) {System.out.print("0");}
        System.out.print(NumberOf1Cost+" ");
        if(NumberOf2Cost<10) {System.out.print("0");}
        System.out.print(NumberOf2Cost+" ");
        if(NumberOf3Cost<10) {System.out.print("0");}
        System.out.print(NumberOf3Cost+" ");
        if(NumberOfBolts<10) {System.out.print("0");}
        System.out.print(NumberOfBolts+" ");
        if(NumberOfLands<10) {System.out.print("0");}
        System.out.print(NumberOfLands);
        System.out.print(" ");
    }
 
    void SetDeck (int Nr1Cost, int Nr2Cost, int Nr3Cost, int NrBolts, int NrLands) {
        NumberOf1Cost=Nr1Cost;
        NumberOf2Cost=Nr2Cost;
        NumberOf3Cost=Nr3Cost;
        NumberOfBolts=NrBolts;
        NumberOfLands=NrLands;
    }
   
    int NrOfCards(){
        return NumberOf1Cost+NumberOf2Cost+NumberOf3Cost+NumberOfBolts+NumberOfLands;
    }
   
    int DrawCard (){
            Random generator = new Random();
            int RandomIntegerBetweenOneAndDeckSize=generator.nextInt( this.NrOfCards() )+1;
            int CardType=0;
            int OneCostCutoff=NumberOf1Cost;
            int TwoCostCutoff=OneCostCutoff+NumberOf2Cost;
            int ThreeCostCutoff=TwoCostCutoff+NumberOf3Cost;
            int BoltCutoff=ThreeCostCutoff+NumberOfBolts;
            int LandCutoff=BoltCutoff+NumberOfLands;
           
            if (RandomIntegerBetweenOneAndDeckSize<=OneCostCutoff) {CardType=1; this.NumberOf1Cost--;}
            if (RandomIntegerBetweenOneAndDeckSize>OneCostCutoff && RandomIntegerBetweenOneAndDeckSize<=TwoCostCutoff) {CardType=2; this.NumberOf2Cost--;}
            if (RandomIntegerBetweenOneAndDeckSize>TwoCostCutoff && RandomIntegerBetweenOneAndDeckSize<=ThreeCostCutoff) {CardType=3; this.NumberOf3Cost--;}
            if (RandomIntegerBetweenOneAndDeckSize>ThreeCostCutoff && RandomIntegerBetweenOneAndDeckSize<=BoltCutoff) {CardType=4; this.NumberOfBolts--;}
            if (RandomIntegerBetweenOneAndDeckSize>BoltCutoff && RandomIntegerBetweenOneAndDeckSize<=LandCutoff) {CardType=5; this.NumberOfLands--;}
            return CardType;
    }
   
}//end of Deck