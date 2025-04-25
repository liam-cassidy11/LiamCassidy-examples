extern crate rand;
extern crate num_bigint;
extern crate lazy_static;
extern crate num_traits;

use lazy_static::lazy_static;
use num_bigint::{BigInt, RandBigInt, ToBigInt};
use num_traits::{One, Zero};
use rand::rngs::OsRng;

/**
 * Struct to store x and y value of each share
 */
#[derive(Debug)]
pub struct Share {
    pub x_val: BigInt,
    pub y_val: BigInt,
}

const PRIME_MODULUS: &str = "115792089237316195423570985008687907853269984665640564039457584007913129639319";

lazy_static! {
    static ref PRIME: BigInt = PRIME_MODULUS.parse().unwrap();
}

/// Retrieves a large prime number
fn generate_prime() -> BigInt {
    PRIME_MODULUS.parse().unwrap()
}


fn share_reconstruction(k: usize, x_values: &[BigInt], y_values: &[BigInt], p: &BigInt) -> BigInt {
    let mut secret = BigInt::from(0);

    for i in 0..k {
        let mut numerator = BigInt::one();
        let mut denominator = BigInt::one();

        for j in 0..k {
            if j != i {
                numerator = (numerator * x_values[j].clone()) % p;
                denominator = (denominator * (x_values[j].clone() - x_values[i].clone())) % p;
            }
        }
        // Compute the modular inverse of the full denominator
        let denominator_inv = denominator
            .modinv(p)
            .expect("Modular inverse not possible");

        // Compute the Lagrange coefficient for share i
        let coefficient = (&numerator * &denominator_inv) % p;
        // Multiply the share's y value by its coefficient
        let term = (&y_values[i] * coefficient) % p;
        secret = (secret + term) % p;
    }
    secret
}

fn main() {
    // Use OSRng
    let mut rng = OsRng;

    // Create secret and prime
    let test_prime = generate_prime();
    let secret = BigInt::from(290604); //bigint has a from bytes function that should help a lot

    //add secret as the last element of polynomial
    let mut coefficients = vec![secret.clone() % &test_prime];
    //println!("Mod {}, prime: {}",(secret.clone() % &test_prime),&test_prime);

    
     // create 2 random large coefficeints and add to list
    let high = 10000.to_bigint().unwrap();
    let low = BigInt::from(0);
    coefficients.push(rng.gen_bigint_range(&low, &high) % &test_prime);

    // Arbitrary x values of 1 and 2
    let x_val1 = BigInt::from(1);
    let x_val2 = BigInt::from(2);

    // y values for function
    let y_val1 = evaluate_polynomial(&coefficients, &x_val1, &test_prime);
    let y_val2 = evaluate_polynomial(&coefficients, &x_val2, &test_prime);

    // Create shares
    let share1 = Share { x_val: x_val1, y_val: y_val1 };
    let share2 = Share { x_val: x_val2, y_val: y_val2 };

    // Print share values
    println!("X1 {} | Y1 {}", share1.x_val, share1.y_val);
    println!("X2 {} | Y2 {}", share2.x_val, share2.y_val); 

    // Test share reconstruction
    let x_values = vec![share1.x_val, share2.x_val];
    let y_values = vec![share1.y_val, share2.y_val];
    let k = x_values.len();

    let recovered_secret = share_reconstruction(k, &x_values, &y_values, &test_prime);

    println!("Original secret: {}", secret);
    println!("Reconstructed key: {}", recovered_secret);
}

/**
 * Uses Horner's Method to evaluate polynomial at x
 */
fn evaluate_polynomial(coefficients: &[BigInt], x: &BigInt, prime: &BigInt ) -> BigInt 
{
    // interates coef list in reverse, starting at secret value
    coefficients.iter().rev().fold(BigInt::from(0), |acc, coeff| 
    {
        //multiplies accumulated value * x + each coefficient all mod our prime number
        (acc * x + coeff) % prime
    })
}
