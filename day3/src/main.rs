mod item {
    #[derive(Debug, Copy, Clone, PartialEq, Eq, Hash)]
    pub(crate) struct Item(u8);

    impl TryFrom<u8> for Item {
        type Error = String;

        fn try_from(value: u8) -> Result<Self, Self::Error> {
            match value {
                b'a'..=b'z' | b'A'..=b'Z' => Ok(Item(value)),
                _ => Err(format!("{} Not a valid item", value as char)),
            }
        }
    }
    impl Item {
        pub(crate) fn score(self) -> usize {
            match self {
                Item(b'a'..=b'z') => 1 + (self.0 - b'a') as usize,
                Item(b'A'..=b'Z') => 27 + (self.0 - b'A') as usize,
                _ => unreachable!(),
            }
        }
    }
}

use im::HashSet;
use item::Item;
use itertools::Itertools;

fn part_1() -> Result<(), String> {
    let sum: usize = include_str!("../../inputs/3_input")
        .lines()
        .map(|line| -> Result<_, String> {
            let (first, second) = line.split_at(line.len() / 2);
            let first_items = first
                .bytes()
                .map(|b| b.try_into().unwrap())
                .collect::<HashSet<Item>>();
            itertools::process_results(second.bytes().map(Item::try_from), |mut it| {
                it.find(|&item| first_items.contains(&item))
                    .map(|item| item.score())
                    .ok_or_else(|| "No common items".to_string())
            })?
        })
        .sum::<Result<usize, String>>()?;
    dbg!(sum);
    Ok(())
}

fn part_2() -> Result<(), String> {
    let sum: usize = include_str!("../../inputs/3_input")
        .lines()
        .map(|line| {
            line.bytes()
                .map(|b| b.try_into().unwrap())
                .collect::<HashSet<Item>>()
        })
        .chunks(3)
        .into_iter()
        .map(|chunk| {
            chunk
                .reduce(|a, b| a.intersection(b))
                .expect("Always 3 chunks")
                .iter()
                .next()
                .expect("Always 1 item in common")
                .score()
        })
        .sum();
    dbg!(sum);
    Ok(())
}
fn main() -> Result<(), String> {
    part_1()?;
    part_2()?;
    Ok(())
}
