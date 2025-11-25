'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter, usePathname } from 'next/navigation';
import {
  Home,
  Settings,
  UserCircle,
  ChevronLeft,
  ChevronRight,
  Bell,
  LogOut,
  SunMedium,
  Gauge,
  Cpu,
  LineChart,
  Zap,
  Sparkles,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import { useAuthStore, getFullName, formatRole } from '@/lib/store/auth-store';

interface SidebarItem {
  name: string;
  href: string;
  icon: React.ElementType;
  badge?: string;
  children?: SidebarItem[];
}

const navigationItems: SidebarItem[] = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: Home,
  },
  {
    name: 'PV Performance',
    href: '/dashboard/pv',
    icon: Gauge,
    children: [
      {
        name: 'Overview',
        href: '/dashboard/pv',
        icon: Gauge,
      },
      {
        name: 'Forecast',
        href: '/dashboard/pv/forecast',
        icon: LineChart,
      },
      {
        name: 'Soiling Index',
        href: '/dashboard/pv/soiling',
        icon: Sparkles,
      },
      {
        name: 'Energy Loss',
        href: '/dashboard/pv/losses',
        icon: Zap,
      },
    ],
  },
  {
    name: 'Devices',
    href: '/dashboard/devices',
    icon: Cpu,
    children: [
      {
        name: 'My Devices',
        href: '/dashboard/devices',
        icon: Cpu,
      },
      {
        name: 'Register Device',
        href: '/dashboard/devices/register',
        icon: Cpu,
      },
      {
        name: 'Device Health',
        href: '/dashboard/devices/health',
        icon: Cpu,
      },
    ],
  },
  {
    name: 'Profile',
    href: '/dashboard/profile',
    icon: UserCircle,
  },
  {
    name: 'Notifications',
    href: '/dashboard/notifications',
    icon: Bell,
  },
  {
    name: 'Settings',
    href: '/dashboard/settings',
    icon: Settings,
  },
];

export function Sidebar() {
  const router = useRouter();
  const pathname = usePathname();
  const { user, logout } = useAuthStore();

  const [isCollapsed, setIsCollapsed] = useState(false);
  const [expandedItems, setExpandedItems] = useState<string[]>([]);

  const toggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
    if (!isCollapsed) {
      // When collapsing, close all expanded items
      setExpandedItems([]);
    }
  };

  const toggleExpanded = (itemName: string) => {
    setExpandedItems((prev) =>
      prev.includes(itemName)
        ? prev.filter((name) => name !== itemName)
        : [...prev, itemName]
    );
  };

  const getInitials = (fullName: string): string => {
    const names = fullName.trim().split(' ');
    if (names.length === 0) return 'U';
    if (names.length === 1) return names[0].substring(0, 2).toUpperCase();
    return (names[0][0] + names[names.length - 1][0]).toUpperCase();
  };

  const isActiveItem = (item: SidebarItem): boolean => {
    if (pathname === item.href) return true;
    if (item.children) {
      return item.children.some((child) => pathname === child.href);
    }
    return false;
  };

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  const fullName = getFullName(user);
  const userInitials = getInitials(fullName);
  const userRole = user ? formatRole(user.role) : '';

  return (
    <TooltipProvider delayDuration={0}>
      <div
        className={cn(
          'flex flex-col h-screen bg-background border-r transition-all duration-300 ease-in-out',
          isCollapsed ? 'w-16' : 'w-64'
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <div className="flex items-center gap-2 overflow-hidden">
            <SunMedium className="h-6 w-6 text-primary flex-shrink-0" />
            {!isCollapsed && (
              <span className="font-bold text-lg whitespace-nowrap">
                SREMS-TN
              </span>
            )}
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleCollapse}
            className="flex-shrink-0"
          >
            {isCollapsed ? (
              <ChevronRight className="h-4 w-4" />
            ) : (
              <ChevronLeft className="h-4 w-4" />
            )}
          </Button>
        </div>

        {/* User Section */}
        <div className="p-4 border-b">
          {isCollapsed ? (
            <Tooltip>
              <TooltipTrigger asChild>
                <div className="flex justify-center">
                  <Avatar className="h-10 w-10">
                    <AvatarFallback className="bg-primary/10 text-primary font-semibold">
                      {userInitials}
                    </AvatarFallback>
                  </Avatar>
                </div>
              </TooltipTrigger>
              <TooltipContent side="right" className="flex flex-col gap-1">
                <p className="font-semibold">{fullName}</p>
                <p className="text-xs text-muted-foreground">{user?.email}</p>
                <Badge variant="secondary" className="mt-1 w-fit">
                  {userRole}
                </Badge>
              </TooltipContent>
            </Tooltip>
          ) : (
            <div className="flex items-center gap-3">
              <Avatar className="h-10 w-10">
                <AvatarFallback className="bg-primary/10 text-primary font-semibold">
                  {userInitials}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 overflow-hidden">
                <p className="font-semibold text-sm truncate">{fullName}</p>
                <p className="text-xs text-muted-foreground truncate">
                  {user?.email}
                </p>
                <Badge variant="secondary" className="mt-1 text-xs">
                  {userRole}
                </Badge>
              </div>
            </div>
          )}
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-2 space-y-1">
          {navigationItems.map((item) => (
            <div key={item.name}>
              {isCollapsed ? (
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      className={cn(
                        'w-full justify-center',
                        isActiveItem(item) &&
                          'bg-primary/10 text-primary hover:bg-primary/20'
                      )}
                      asChild={!item.children}
                      onClick={() => {
                        if (item.children) {
                          setIsCollapsed(false);
                          toggleExpanded(item.name);
                        }
                      }}
                    >
                      {item.children ? (
                        <div>
                          <item.icon className="h-4 w-4" />
                        </div>
                      ) : (
                        <Link href={item.href}>
                          <item.icon className="h-4 w-4" />
                        </Link>
                      )}
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent side="right">
                    <p>{item.name}</p>
                  </TooltipContent>
                </Tooltip>
              ) : (
                <>
                  {item.children ? (
                    <Button
                      variant="ghost"
                      className={cn(
                        'w-full justify-between',
                        isActiveItem(item) &&
                          'bg-primary/10 text-primary hover:bg-primary/20'
                      )}
                      onClick={() => toggleExpanded(item.name)}
                    >
                      <div className="flex items-center gap-2">
                        <item.icon className="h-4 w-4" />
                        <span className="text-sm">{item.name}</span>
                      </div>
                      <ChevronRight
                        className={cn(
                          'h-4 w-4 transition-transform duration-200',
                          expandedItems.includes(item.name) && 'rotate-90'
                        )}
                      />
                    </Button>
                  ) : (
                    <Button
                      variant="ghost"
                      className={cn(
                        'w-full justify-start gap-2',
                        isActiveItem(item) &&
                          'bg-primary/10 text-primary hover:bg-primary/20'
                      )}
                      asChild
                    >
                      <Link href={item.href}>
                        <item.icon className="h-4 w-4" />
                        <span className="text-sm">{item.name}</span>
                        {item.badge && (
                          <Badge variant="secondary" className="ml-auto">
                            {item.badge}
                          </Badge>
                        )}
                      </Link>
                    </Button>
                  )}

                  {/* Submenu */}
                  {item.children && expandedItems.includes(item.name) && (
                    <div className="ml-4 mt-1 space-y-1 overflow-hidden transition-all duration-200">
                      {item.children.map((child) => (
                        <Button
                          key={child.name}
                          variant="ghost"
                          size="sm"
                          className={cn(
                            'w-full justify-start gap-2 pl-6',
                            pathname === child.href &&
                              'bg-primary/10 text-primary hover:bg-primary/20'
                          )}
                          asChild
                        >
                          <Link href={child.href}>
                            <child.icon className="h-3 w-3" />
                            <span className="text-xs">{child.name}</span>
                          </Link>
                        </Button>
                      ))}
                    </div>
                  )}
                </>
              )}
            </div>
          ))}
        </nav>

        <Separator />

        {/* Logout */}
        <div className="p-2">
          {isCollapsed ? (
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={handleLogout}
                  className="w-full hover:bg-destructive/10 hover:text-destructive"
                >
                  <LogOut className="h-4 w-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right">
                <p>Logout</p>
              </TooltipContent>
            </Tooltip>
          ) : (
            <Button
              variant="ghost"
              onClick={handleLogout}
              className="w-full justify-start gap-2 hover:bg-destructive/10 hover:text-destructive"
            >
              <LogOut className="h-4 w-4" />
              <span className="text-sm">Logout</span>
            </Button>
          )}
        </div>
      </div>
    </TooltipProvider>
  );
}
