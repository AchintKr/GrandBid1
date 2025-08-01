"use client";

import React, { useEffect, useRef, useState } from 'react';
import { cn } from '@/lib/utils';

export const GlowingCard = ({
  children,
  className,
  glowColor = "#f59e0b", // amber-500 for magical theme
  hoverEffect = true,
  ...props
}) => {
  return (
    <div
      className={cn(
        "relative flex-1 min-w-[14rem] p-6 rounded-2xl text-white",
        "bg-slate-800/80 border border-slate-700/50 backdrop-blur-sm",
        "transition-all duration-300 ease-out",
        className
      )}
      style={{
        '--glow-color': glowColor,
      }}
      {...props}
    >
      {children}
    </div>
  );
};

export const GlowingCards = ({
  children,
  className,
  enableGlow = true,
  glowRadius = 25,
  glowOpacity = 0.8,
  animationDuration = 300,
  enableHover = true,
  gap = "2rem",
  maxWidth = "75rem",
  padding = "0",
  backgroundColor,
  borderRadius = "1rem",
  responsive = true,
  customTheme,
}) => {
  const containerRef = useRef(null);
  const overlayRef = useRef(null);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [showOverlay, setShowOverlay] = useState(false);

  useEffect(() => {
    const container = containerRef.current;
    const overlay = overlayRef.current;

    if (!container || !overlay || !enableGlow) return;

    const handleMouseMove = (e) => {
      const rect = container.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      setMousePosition({ x, y });
      setShowOverlay(true);

      overlay.style.setProperty('--x', x + 'px');
      overlay.style.setProperty('--y', y + 'px');
      overlay.style.setProperty('--opacity', glowOpacity.toString());
    };

    const handleMouseLeave = () => {
      setShowOverlay(false);
      overlay.style.setProperty('--opacity', '0');
    };

    container.addEventListener('mousemove', handleMouseMove);
    container.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      container.removeEventListener('mousemove', handleMouseMove);
      container.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, [enableGlow, glowOpacity]);

  const containerStyle = {
    '--gap': gap,
    '--max-width': maxWidth,
    '--padding': padding,
    '--border-radius': borderRadius,
    '--animation-duration': animationDuration + 'ms',
    '--glow-radius': glowRadius + 'rem',
    '--glow-opacity': glowOpacity,
    backgroundColor: backgroundColor || undefined,
    ...customTheme,
  };

  return (
    <div
      className={cn("relative w-full", className)}
      style={containerStyle}
    >
      <div
        ref={containerRef}
        className={cn(
          "relative max-w-[var(--max-width)] mx-auto"
        )}
        style={{ padding: "var(--padding)" }}
      >
        <div
          className={cn(
            "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-[var(--gap)]",
            responsive && "grid-cols-1 md:grid-cols-2 lg:grid-cols-4"
          )}
        >
          {children}
        </div>

        {enableGlow && (
          <div
            ref={overlayRef}
            className={cn(
              "absolute inset-0 pointer-events-none select-none",
              "opacity-0 transition-all duration-[var(--animation-duration)] ease-out"
            )}
            style={{
              WebkitMask: `radial-gradient(var(--glow-radius) var(--glow-radius) at var(--x, 0) var(--y, 0), #000 1%, transparent 50%)`,
              mask: `radial-gradient(var(--glow-radius) var(--glow-radius) at var(--x, 0) var(--y, 0), #000 1%, transparent 50%)`,
              opacity: showOverlay ? 'var(--opacity)' : '0',
            }}
          >
            <div
              className={cn(
                "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-[var(--gap)] max-w-[var(--max-width)] mx-auto",
                responsive && "grid-cols-1 md:grid-cols-2 lg:grid-cols-4"
              )}
              style={{ padding: "var(--padding)" }}
            >
              {React.Children.map(children, (child, index) => {
                if (React.isValidElement(child) && child.type === GlowingCard) {
                  const cardGlowColor = child.props.glowColor || "#f59e0b";
                  return React.cloneElement(child, {
                    className: cn(
                      child.props.className,
                      "bg-opacity-15 dark:bg-opacity-15",
                      "border-opacity-100 dark:border-opacity-100"
                    ),
                    style: {
                      ...child.props.style,
                      backgroundColor: cardGlowColor + "15",
                      borderColor: cardGlowColor,
                      boxShadow: `0 0 0 1px inset ${cardGlowColor}`,
                    },
                  });
                }
                return child;
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default GlowingCards;
