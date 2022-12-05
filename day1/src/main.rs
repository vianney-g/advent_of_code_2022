use itertools::Itertools;

fn main() {
    let input = include_str!("../../inputs/1_input");
    let lines = input.lines().map(|v| v.parse::<u64>().ok());
    let max = lines
        .batching(|it| {
            let mut sum = None;
            while let Some(Some(v)) = it.next() {
                sum = Some(sum.unwrap_or(0) + v);
            }
            sum
        })
        .max();

    println!("{:?}", max);
}
