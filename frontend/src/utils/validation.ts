/**
 * Check an email address and a password against Zod schemas.
 *
 * No module in the tree calls either function, so neither the registration form nor
 * any other input runs these rules. Both return only the boolean outcome and
 * discard the messages their schemas carry, so a caller cannot tell which rule
 * failed.
 *
 * `zod` is imported and `frontend/package.json` does not declare it.
 *
 * @see ./README.md
 */
import { z } from 'zod';

/**
 * Report whether a string is a syntactically valid email address.
 *
 * @param email - The address to check.
 * @returns True when Zod's email rule accepts the string.
 */
export const validateEmail = (email: string): boolean => {
  const emailSchema = z.string().email();
  return emailSchema.safeParse(email).success;
};

/**
 * Report whether a password meets the length and character policy.
 *
 * The policy is at least eight characters with a lowercase letter, an uppercase
 * letter, a digit and one of `@$!%*?&`. The pattern also restricts the password to
 * those character classes, so a space or any other punctuation fails.
 *
 * @param password - The password to check.
 * @returns True when the password satisfies every rule.
 */
export const validatePassword = (password: string): boolean => {
  const passwordSchema = z.string()
    .min(8, { message: "Password must be at least 8 characters long" })
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/, {
      message: "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
    });
  return passwordSchema.safeParse(password).success;
};