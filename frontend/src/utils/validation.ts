/** Validate email addresses and passwords with Zod.
 *
 * zod is imported but undeclared in frontend/package.json.
 */
import { z } from 'zod';

/**
 * Report whether a string is a valid email address.
 *
 * @param email - The address to check.
 * @returns `true` when the address parses, and `false` otherwise. The parser message is discarded.
 */
export const validateEmail = (email: string): boolean => {
  const emailSchema = z.string().email();
  return emailSchema.safeParse(email).success;
};

/**
 * Report whether a password satisfies the local policy.
 *
 * The policy requires at least eight characters and at least one lowercase letter,
 * one uppercase letter, one digit, and one character from `@$!%*?&`.
 * The pattern also restricts the whole password to letters, digits and `@$!%*?&`, so any
 * other symbol is rejected. `Passw0rd@#` satisfies all four class rules and still fails,
 * because `#` falls outside the allowed set.
 *
 * @param password - The password to check.
 * @returns `true` when the password parses, and `false` otherwise. Both policy messages
 * are discarded.
 */
export const validatePassword = (password: string): boolean => {
  const passwordSchema = z.string()
    .min(8, { message: "Password must be at least 8 characters long" })
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/, {
      message: "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
    });
  return passwordSchema.safeParse(password).success;
};