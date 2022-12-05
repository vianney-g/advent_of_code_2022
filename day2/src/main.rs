use core::str::FromStr;

#[derive(Debug, Clone, Copy)]
enum Move {
    Rock,
    Paper,
    Scissors,
}

#[derive(Debug, Clone, Copy)]
enum RoundResult {
    Win,
    Draw,
    Loss,
}

impl RoundResult {
    fn points(self) -> usize {
        match self {
            RoundResult::Win => 6,
            RoundResult::Draw => 3,
            RoundResult::Loss => 0,
        }
    }
}

impl TryFrom<char> for Move {
    type Error = &'static str;
    fn try_from(c: char) -> Result<Self, Self::Error> {
        match c {
            'A' | 'X' => Ok(Move::Rock),
            'B' | 'Y' => Ok(Move::Paper),
            'C' | 'Z' => Ok(Move::Scissors),
            _ => Err("Not a valid move {c:?}"),
        }
    }
}

impl Move {
    fn points(self) -> usize {
        match self {
            Move::Rock => 1,
            Move::Paper => 2,
            Move::Scissors => 3,
        }
    }
    fn beats(self, theirs: Move) -> bool {
        match (self, theirs) {
            (Move::Rock, Move::Scissors) => true,
            (Move::Scissors, Move::Paper) => true,
            (Move::Paper, Move::Rock) => true,
            (_, _) => false,
        }
    }
}

#[derive(Debug, Clone, Copy)]
struct Round {
    ours: Move,
    theirs: Move,
}

impl FromStr for Round {
    type Err = &'static str;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut chars = s.chars();
        let (Some(theirs), Some(' '), Some(ours), None) =
            (chars.next(), chars.next(), chars.next(), chars.next()) else {
            return Err("Bad line {:s}");
        };
        Ok(Self {
            ours: ours.try_into()?,
            theirs: theirs.try_into()?,
        })
    }
}

impl Round {
    fn result(self) -> RoundResult {
        if self.ours.beats(self.theirs) {
            RoundResult::Win
        } else if self.theirs.beats(self.ours) {
            RoundResult::Loss
        } else {
            RoundResult::Draw
        }
    }

    fn points(self) -> usize {
        self.ours.points() + self.result().points()
    }
}

fn main() {
    let input = include_str!("../../inputs/2_input");
    let sum: usize = input
        .lines()
        .map(|line| line.parse().unwrap())
        .map(Round::points)
        .sum();
    println!("{sum:?}");
}
