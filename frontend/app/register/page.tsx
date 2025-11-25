'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { authAPI } from '@/lib/api/auth';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { SunMedium, Loader2, CheckCircle2, Eye, EyeOff, User, Wrench, Shield } from 'lucide-react';

type UserRole = 'particulier' | 'technician' | 'operator';

interface RoleSpecificFields {
  particulier: {
    system_capacity_kwp: string;
    has_battery: boolean;
    address: string;
  };
  technician: {
    company_name: string;
    certifications: string[];
  };
  operator: {
    department: string;
    access_level: string;
  };
}

const roleIcons = {
  particulier: User,
  technician: Wrench,
  operator: Shield,
};

const roleDescriptions = {
  particulier: 'Individual solar system owner',
  technician: 'Solar system maintenance professional',
  operator: 'System operator or administrator',
};

export default function RegisterPage() {
  const router = useRouter();
  
  // Form fields
  const [name, setName] = useState('');
  const [surname, setSurname] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState<UserRole>('particulier');
  
  // Role-specific fields
  const [roleFields, setRoleFields] = useState<RoleSpecificFields>({
    particulier: {
      system_capacity_kwp: '',
      has_battery: false,
      address: '',
    },
    technician: {
      company_name: '',
      certifications: [],
    },
    operator: {
      department: '',
      access_level: 'read-only',
    },
  });
  
  // UI states
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  
  // OTP Dialog states
  const [showOtpDialog, setShowOtpDialog] = useState(false);
  const [otpCode, setOtpCode] = useState('');
  const [isVerifying, setIsVerifying] = useState(false);
  const [verificationError, setVerificationError] = useState('');

  // Password validation
  const validatePassword = (pwd: string): string[] => {
    const errors: string[] = [];
    if (pwd.length < 8) errors.push('At least 8 characters');
    if (!/[A-Z]/.test(pwd)) errors.push('One uppercase letter');
    if (!/[a-z]/.test(pwd)) errors.push('One lowercase letter');
    if (!/\d/.test(pwd)) errors.push('One digit');
    return errors;
  };

  const passwordErrors = password ? validatePassword(password) : [];
  const passwordsMatch = password && confirmPassword && password === confirmPassword;

  const updateRoleField = (field: string, value: any) => {
    setRoleFields(prev => ({
      ...prev,
      [role]: {
        ...prev[role],
        [field]: value,
      },
    }));
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validate passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    // Validate password strength
    if (passwordErrors.length > 0) {
      setError('Password does not meet requirements');
      return;
    }

    setIsLoading(true);

    try {
      // Prepare registration data with role-specific fields
      const registrationData = {
        name: name.trim(),
        surname: surname.trim(),
        phone: phone.trim(),
        email: email.trim(),
        password,
        role,
        ...roleFields[role],
      };

      const response = await authAPI.register(registrationData);

      // Show OTP dialog
      setShowOtpDialog(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleVerifyOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    setVerificationError('');

    if (otpCode.length !== 6) {
      setVerificationError('OTP code must be 6 digits');
      return;
    }

    setIsVerifying(true);

    try {
      const response = await authAPI.verifyOTP(phone.trim(), otpCode);

      // Verification successful - redirect to login
      setShowOtpDialog(false);
      router.push('/login?message=registration_success');
    } catch (err) {
      setVerificationError(err instanceof Error ? err.message : 'Invalid OTP code. Please try again.');
    } finally {
      setIsVerifying(false);
    }
  };

  const handleResendOtp = async () => {
    setVerificationError('');
    setIsLoading(true);

    try {
      const registrationData = {
        name: name.trim(),
        surname: surname.trim(),
        phone: phone.trim(),
        email: email.trim(),
        password,
        role,
        ...roleFields[role],
      };

      await authAPI.register(registrationData);
      setVerificationError('');
      alert('New OTP code sent successfully!');
    } catch (err) {
      setVerificationError(err instanceof Error ? err.message : 'Failed to resend OTP');
    } finally {
      setIsLoading(false);
    }
  };

  const renderRoleSpecificFields = () => {
    switch (role) {
      case 'particulier':
        return (
          <div className="space-y-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border">
            <h3 className="font-medium text-blue-900 dark:text-blue-100">Solar System Details</h3>
            <div className="space-y-2">
              <Label htmlFor="system_capacity_kwp">PV System Capacity (kWp)</Label>
              <Input
                id="system_capacity_kwp"
                type="number"
                step="0.1"
                placeholder="5.0"
                value={roleFields.particulier.system_capacity_kwp}
                onChange={(e) => updateRoleField('system_capacity_kwp', e.target.value)}
                disabled={isLoading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="has_battery">Battery Storage</Label>
              <div className="flex gap-4">
                <div className="flex items-center space-x-2">
                  <input
                    type="radio"
                    id="battery-yes"
                    name="has_battery"
                    value="yes"
                    checked={roleFields.particulier.has_battery}
                    onChange={(e) => updateRoleField('has_battery', e.target.value === 'yes')}
                    className="text-primary"
                  />
                  <Label htmlFor="battery-yes" className="cursor-pointer">Yes</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <input
                    type="radio"
                    id="battery-no"
                    name="has_battery"
                    value="no"
                    checked={!roleFields.particulier.has_battery}
                    onChange={(e) => updateRoleField('has_battery', e.target.value === 'yes')}
                    className="text-primary"
                  />
                  <Label htmlFor="battery-no" className="cursor-pointer">No</Label>
                </div>
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="address">Address</Label>
              <Input
                id="address"
                placeholder="City, Tunisia"
                value={roleFields.particulier.address}
                onChange={(e) => updateRoleField('address', e.target.value)}
                disabled={isLoading}
              />
            </div>
          </div>
        );

      case 'technician':
        return (
          <div className="space-y-4 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border">
            <h3 className="font-medium text-green-900 dark:text-green-100">Professional Details</h3>
            <div className="space-y-2">
              <Label htmlFor="company_name">Company Name</Label>
              <Input
                id="company_name"
                placeholder="SolarTech Maintenance Ltd"
                value={roleFields.technician.company_name}
                onChange={(e) => updateRoleField('company_name', e.target.value)}
                disabled={isLoading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="certifications">Certifications (comma-separated)</Label>
              <Input
                id="certifications"
                placeholder="IEC 61215, SMA Certified, Fronius Certified"
                value={roleFields.technician.certifications.join(', ')}
                onChange={(e) => updateRoleField('certifications', e.target.value.split(',').map(s => s.trim()).filter(s => s))}
                disabled={isLoading}
              />
            </div>
          </div>
        );

      case 'operator':
        return (
          <div className="space-y-4 p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border">
            <h3 className="font-medium text-purple-900 dark:text-purple-100">Access Details</h3>
            <div className="space-y-2">
              <Label htmlFor="department">Department</Label>
              <Input
                id="department"
                placeholder="Operations, Maintenance, Administration"
                value={roleFields.operator.department}
                onChange={(e) => updateRoleField('department', e.target.value)}
                disabled={isLoading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="access_level">Access Level</Label>
              <div className="flex gap-4">
                <div className="flex items-center space-x-2">
                  <input
                    type="radio"
                    id="access-readonly"
                    name="access_level"
                    value="read-only"
                    checked={roleFields.operator.access_level === 'read-only'}
                    onChange={(e) => updateRoleField('access_level', e.target.value)}
                    className="text-primary"
                  />
                  <Label htmlFor="access-readonly" className="cursor-pointer">Read Only</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <input
                    type="radio"
                    id="access-full"
                    name="access_level"
                    value="full"
                    checked={roleFields.operator.access_level === 'full'}
                    onChange={(e) => updateRoleField('access_level', e.target.value)}
                    className="text-primary"
                  />
                  <Label htmlFor="access-full" className="cursor-pointer">Full Access</Label>
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <>
      <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 p-4">
        <Card className="w-full max-w-2xl shadow-lg">
          <CardHeader className="space-y-1 text-center">
            <div className="flex justify-center mb-4">
              <div className="p-3 bg-primary/10 rounded-full">
                <SunMedium className="h-10 w-10 text-primary" />
              </div>
            </div>
            <CardTitle className="text-2xl font-bold">Create Account</CardTitle>
            <CardDescription>
              Join SREMS-TN to manage your solar energy system
            </CardDescription>
          </CardHeader>
          <form onSubmit={handleRegister}>
            <CardContent className="space-y-6">
              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {/* Basic Information */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium">Basic Information</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="name">First Name *</Label>
                    <Input
                      id="name"
                      placeholder="Ahmed"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      required
                      disabled={isLoading}
                      minLength={2}
                      maxLength={100}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="surname">Last Name *</Label>
                    <Input
                      id="surname"
                      placeholder="Ben Salem"
                      value={surname}
                      onChange={(e) => setSurname(e.target.value)}
                      required
                      disabled={isLoading}
                      minLength={2}
                      maxLength={100}
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="phone">Phone Number *</Label>
                  <Input
                    id="phone"
                    type="tel"
                    placeholder="+216 98 765 432"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    required
                    disabled={isLoading}
                  />
                  <p className="text-xs text-muted-foreground">
                    Tunisia format: +216 XX XXX XXX
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email *</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="ahmed@example.tn"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    disabled={isLoading}
                  />
                </div>
              </div>

              {/* Role Selection */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium">Select Your Role</h3>
                <div className="grid grid-cols-1 gap-4">
                  {Object.entries(roleDescriptions).map(([roleKey, description]) => {
                    const IconComponent = roleIcons[roleKey as UserRole];
                    return (
                      <div key={roleKey} className="flex items-center space-x-3 p-4 border rounded-lg hover:bg-accent cursor-pointer">
                        <input
                          type="radio"
                          id={roleKey}
                          name="role"
                          value={roleKey}
                          checked={role === roleKey}
                          onChange={(e) => setRole(e.target.value as UserRole)}
                          className="text-primary"
                        />
                        <IconComponent className="h-5 w-5 text-primary" />
                        <div className="flex-1">
                          <Label htmlFor={roleKey} className="font-medium capitalize cursor-pointer">
                            {roleKey}
                          </Label>
                          <p className="text-sm text-muted-foreground">{description}</p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Role-Specific Fields */}
              {renderRoleSpecificFields()}

              {/* Password Fields */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium">Security</h3>
                <div className="space-y-2">
                  <Label htmlFor="password">Password *</Label>
                  <div className="relative">
                    <Input
                      id="password"
                      type={showPassword ? 'text' : 'password'}
                      placeholder="Create a strong password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      disabled={isLoading}
                      minLength={8}
                      className="pr-10"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    >
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  </div>
                  {password && passwordErrors.length > 0 && (
                    <div className="text-xs space-y-1">
                      <p className="text-muted-foreground">Password must contain:</p>
                      <ul className="space-y-0.5">
                        {passwordErrors.map((err, idx) => (
                          <li key={idx} className="text-red-500">• {err}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">Confirm Password *</Label>
                  <div className="relative">
                    <Input
                      id="confirmPassword"
                      type={showConfirmPassword ? 'text' : 'password'}
                      placeholder="Re-enter your password"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      required
                      disabled={isLoading}
                      minLength={8}
                      className="pr-10"
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    >
                      {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  </div>
                  {confirmPassword && (
                    <p className={`text-xs ${passwordsMatch ? 'text-green-600' : 'text-red-500'}`}>
                      {passwordsMatch ? '✓ Passwords match' : '✗ Passwords do not match'}
                    </p>
                  )}
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex flex-col space-y-4">
              <Button 
                type="submit" 
                className="w-full" 
                disabled={isLoading || passwordErrors.length > 0 || !passwordsMatch}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Creating account...
                  </>
                ) : (
                  'Create Account'
                )}
              </Button>
              <div className="text-sm text-center text-muted-foreground">
                Already have an account?{' '}
                <Link href="/login" className="text-primary font-medium hover:underline">
                  Sign in here
                </Link>
              </div>
            </CardFooter>
          </form>
        </Card>
      </div>

      {/* OTP Verification Dialog */}
      <Dialog open={showOtpDialog} onOpenChange={setShowOtpDialog}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-green-500" />
              Verify Your Phone
            </DialogTitle>
            <DialogDescription>
              We've sent a 6-digit code to <strong>{phone}</strong>. 
              Please enter it below to complete registration.
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleVerifyOtp}>
            <div className="space-y-4 py-4">
              {verificationError && (
                <Alert variant="destructive">
                  <AlertDescription>{verificationError}</AlertDescription>
                </Alert>
              )}
              <div className="space-y-2">
                <Label htmlFor="otp">Verification Code</Label>
                <Input
                  id="otp"
                  type="text"
                  placeholder="000000"
                  value={otpCode}
                  onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                  maxLength={6}
                  className="text-center text-2xl tracking-widest"
                  disabled={isVerifying}
                  required
                />
                <p className="text-xs text-muted-foreground text-center">
                  Code expires in 10 minutes
                </p>
              </div>
            </div>
            <DialogFooter className="flex-col sm:flex-col gap-2">
              <Button type="submit" className="w-full" disabled={isVerifying || otpCode.length !== 6}>
                {isVerifying ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Verifying...
                  </>
                ) : (
                  'Verify & Complete Registration'
                )}
              </Button>
              <Button 
                type="button" 
                variant="outline" 
                className="w-full"
                onClick={handleResendOtp}
                disabled={isLoading}
              >
                Resend Code
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </>
  );
}
