/**
 * Check an email address and a password against Zod schemas, reporting only whether each value
 * satisfies its schema.
 *
 * Both exported functions build a schema and call `safeParse`, then return the `.success` flag, so
 * the configured message strings never reach a caller.
 *
 * The `zod` import does not resolve, because `frontend/package.json` omits the package, so neither
 * check runs as committed. No module under `frontend/src` calls either function today.
 *
 * @see ./README.md for the register covering this directory.
 */
import { z } from 'zod';

/**
 * Report whether a string parses as an email address.
 *
 * @param email - Candidate address checked against a `z.string().email()` schema.
 * @returns `true` when the schema accepts the value and `false` otherwise, read from
 *   `safeParse(...).success`.
 * @remarks The return carries no failure detail, and the undeclared `zod` import stops the check
 *   from running as committed.
 */
export const validateEmail = (email: string): boolean => {
  const emailSchema = z.string().email();
  return emailSchema.safeParse(email).success;
};

/**
 * Report whether a string satisfies the password policy.
 *
 * @param password - Candidate password checked against the schema built in the body.
 * @returns `true` when the schema accepts the value and `false` otherwise, read from
 *   `safeParse(...).success`.
 * @remarks The policy holds six requirements: a minimum of 8 characters, and at least one lowercase
 *   letter, one uppercase letter, one digit and one character from `@$!%*?&`. The anchored
 *   expression also confines the whole value to `[A-Za-z\d@$!%*?&]{8,}`, so a password holding any
 *   character outside that class fails even when it meets the other five. `Passw0rd@#` fails on the
 *   `#` alone.
 *
 *   The return carries only `.success`, so both configured message strings are discarded, and the
 *   undeclared `zod` import stops the check from running as committed.
 */
export const validatePassword = (password: string): boolean => {
  const passwordSchema = z.string()
    .min(8, { message: "Password must be at least 8 characters long" })
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/, {
      message: "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
    });
  return passwordSchema.safeParse(password).success;
};